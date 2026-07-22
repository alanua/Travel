'use strict'

const core = require('@actions/core')
const github = require('@actions/github')
const {DefaultArtifactClient} = require('@actions/artifact')

const sleep = milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds))

async function run() {
  const token = core.getInput('token', {required: true})
  const artifactPath = core.getInput('artifact-path', {required: true})
  const buildVersion = process.env.GITHUB_SHA
  if (!buildVersion) throw new Error('missing_github_sha')

  const artifactClient = new DefaultArtifactClient()
  const uploaded = await artifactClient.uploadArtifact(
    'github-pages',
    [artifactPath],
    {retentionDays: 1}
  )
  if (!uploaded || !uploaded.id) throw new Error('artifact_upload_missing_id')

  const idToken = await core.getIDToken()
  if (!idToken) throw new Error('missing_oidc_token')

  const octokit = github.getOctokit(token)
  const owner = github.context.repo.owner
  const repo = github.context.repo.repo
  const created = await octokit.request('POST /repos/{owner}/{repo}/pages/deployments', {
    owner,
    repo,
    artifact_id: uploaded.id,
    pages_build_version: buildVersion,
    oidc_token: idToken
  })

  const deploymentId = created.data.id || String(created.data.status_url || '').split('/').pop()
  if (!deploymentId) throw new Error('pages_deployment_missing_id')

  const terminalFailures = new Set([
    'deployment_failed',
    'deployment_perms_error',
    'deployment_content_failed',
    'deployment_cancelled',
    'deployment_lost'
  ])

  for (let attempt = 0; attempt < 120; attempt += 1) {
    await sleep(5000)
    const statusResponse = await octokit.request(
      'GET /repos/{owner}/{repo}/pages/deployments/{deploymentId}',
      {owner, repo, deploymentId}
    )
    const status = statusResponse.data.status
    if (status === 'succeed') {
      core.setOutput('deployment-id', deploymentId)
      core.setOutput('page-url', statusResponse.data.page_url || created.data.page_url || '')
      return
    }
    if (terminalFailures.has(status)) throw new Error(`pages_${status}`)
  }

  throw new Error('pages_deployment_timeout')
}

run().catch(error => core.setFailed(error instanceof Error ? error.message : String(error)))

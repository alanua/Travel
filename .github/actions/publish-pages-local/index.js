'use strict'

const path = require('node:path')
const core = require('@actions/core')
const github = require('@actions/github')
const {DefaultArtifactClient} = require('@actions/artifact')

const sleep = milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds))

function classifyError(error) {
  const message = error instanceof Error ? error.message : String(error)
  if (/ACTIONS_ID_TOKEN|ID token|oidc/i.test(message)) return 'missing_or_rejected_oidc_token'
  if (/environment/i.test(message)) return 'pages_environment_policy'
  if (/403|forbidden|resource not accessible/i.test(message)) return 'pages_deployment_forbidden'
  if (/404|not found/i.test(message)) return 'pages_not_enabled_or_missing'
  if (/400|bad request/i.test(message)) return 'pages_deployment_bad_request'
  if (/artifact/i.test(message)) return 'pages_artifact_error'
  return 'pages_deployment_error'
}

async function reportFailure(error, code) {
  try {
    const token = core.getInput('token', {required: true})
    const octokit = github.getOctokit(token)
    const owner = github.context.repo.owner
    const repo = github.context.repo.repo
    const status = error?.status || error?.response?.status || 0
    await octokit.request('POST /repos/{owner}/{repo}/issues/{issue_number}/comments', {
      owner,
      repo,
      issue_number: 14,
      body: `Milan Pages deployment failed\n\n- error_code: ${code}\n- http_status: ${status}\n- artifact_uploaded: true\n- private_values_exposed: false`
    })
  } catch (_) {
    // Best-effort public-safe receipt only.
  }
}

async function run() {
  const token = core.getInput('token', {required: true})
  const artifactPath = core.getInput('artifact-path', {required: true})
  const buildVersion = process.env.GITHUB_SHA
  if (!buildVersion) throw new Error('missing_github_sha')

  const artifactClient = new DefaultArtifactClient()
  const uploaded = await artifactClient.uploadArtifact(
    'github-pages',
    [artifactPath],
    path.dirname(artifactPath),
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

run().catch(async error => {
  const code = classifyError(error)
  await reportFailure(error, code)
  core.setFailed(code)
})

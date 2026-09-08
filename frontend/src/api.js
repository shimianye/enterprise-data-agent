/** 后端接口封装：唯一与 /api 打交道的模块。 */
const BASE = import.meta.env.VITE_API_BASE || '/api'

export class QueryError extends Error {
  constructor(kind, message, detail = null) {
    super(message)
    this.kind = kind      // network | sql_invalid | db_error | llm_error | invalid | unknown
    this.detail = detail
  }
}

function mapError(status, detail) {
  if (status === 400) {
    if (detail?.error === 'sql_invalid') {
      return new QueryError('sql_invalid', '该问题无法生成安全的查询语句，已被安全校验拦截。', detail.violations)
    }
    return new QueryError('db_error', `查询执行失败：${detail?.message || ''}`, detail)
  }
  if (status === 502) return new QueryError('llm_error', '模型服务不可用，请稍后重试。', detail)
  if (status === 422) return new QueryError('invalid', '请求不合法。', detail)
  return new QueryError('unknown', `未知错误（HTTP ${status}）`, detail)
}

export async function postQuery(question) {
  let res
  try {
    res = await fetch(`${BASE}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    })
  } catch (e) {
    throw new QueryError('network', '无法连接后端，请确认服务已启动（默认 http://127.0.0.1:8000）。')
  }
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw mapError(res.status, data.detail)
  return data
}

export async function fetchHealth() {
  try {
    const res = await fetch(`${BASE}/health`)
    return res.ok ? await res.json() : null
  } catch {
    return null
  }
}

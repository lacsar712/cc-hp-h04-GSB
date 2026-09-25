import { test } from 'node:test'
import assert from 'node:assert/strict'
import { viewRows } from './ordering.js'

test('页面不再倒序：直接按接口顺序展示，最新行保持在最前', () => {
  const fromApi = [{ id: 3 }, { id: 2 }, { id: 1 }]
  assert.deepEqual(viewRows(fromApi).map((r) => r.id), [3, 2, 1])
})

test('不修改传入数组本身', () => {
  const fromApi = [{ id: 2 }, { id: 1 }]
  const view = viewRows(fromApi)
  assert.notEqual(view, fromApi)
  assert.deepEqual(view.map((r) => r.id), [2, 1])
})

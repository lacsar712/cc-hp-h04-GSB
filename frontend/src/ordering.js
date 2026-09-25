// 列表展示顺序：接口已按“最新写入排在最前”返回，页面直接采用，
// 不再做二次倒排（曾因 reverse() 把最新行顶到最旧之后）。
export function viewRows(rows) {
  return [...rows]
}

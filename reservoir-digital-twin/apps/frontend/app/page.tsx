import Link from 'next/link'

export default function Home() {
  return (
    <div className="main">
      <h1 className="page-title">欢迎使用</h1>
      
      <div className="grid-3">
        <Link href="/dams" className="card animate-in animate-delay-1" style={{ textDecoration: 'none' }}>
          <div className="card-title">
            🏔️ 水库大坝
          </div>
          <div className="card-content">
            <p>管理水库大坝的基础信息、位置坐标、运行状态等核心数据。</p>
          </div>
        </Link>

        <Link href="/dashboard" className="card animate-in animate-delay-2" style={{ textDecoration: 'none' }}>
          <div className="card-title">
            📊 数据看板
          </div>
          <div className="card-content">
            <p>查看实时监测数据、统计分析图表、告警信息汇总。</p>
          </div>
        </Link>

        <Link href="/alerts" className="card animate-in animate-delay-3" style={{ textDecoration: 'none' }}>
          <div className="card-title">
            🔔 告警中心
          </div>
          <div className="card-content">
            <p>实时监测告警信息，支持告警确认、处理和历史查询。</p>
          </div>
        </Link>

        <Link href="/forecasts" className="card animate-in animate-delay-4" style={{ textDecoration: 'none' }}>
          <div className="card-title">
            📈 预测分析
          </div>
          <div className="card-content">
            <p>基于历史数据和模型算法进行趋势预测和风险评估。</p>
          </div>
        </Link>
      </div>
    </div>
  )
}

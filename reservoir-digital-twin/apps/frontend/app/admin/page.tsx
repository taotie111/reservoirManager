import React from 'react'
import Link from 'next/link'

export default function Admin() {
  const menuItems = [
    { icon: '👥', title: '用户管理', desc: '管理系统用户、角色和权限', href: '#' },
    { icon: '🔐', title: '角色权限', desc: '配置角色权限和访问控制', href: '#' },
    { icon: '📝', title: '日志审计', desc: '查看系统操作日志和审计记录', href: '#' },
    { icon: '⚙️', title: '系统配置', desc: '系统参数配置和功能开关', href: '#' },
    { icon: '🔌', title: '接口管理', desc: '第三方接口配置和监控', href: '#' },
    { icon: '📦', title: '数据管理', desc: '数据备份、导入导出', href: '#' },
  ]

  return (
    <div className="main">
      <h1 className="page-title">系统管理</h1>

      <div className="grid-3">
        {menuItems.map((item, index) => (
          <Link 
            key={index} 
            href={item.href}
            className={`card animate-in animate-delay-${index + 1}`}
            style={{ textDecoration: 'none' }}
          >
            <div className="card-title">
              <span style={{ fontSize: '24px' }}>{item.icon}</span>
            </div>
            <div className="card-content">
              <p style={{ fontWeight: 600, marginBottom: '4px' }}>{item.title}</p>
              <p style={{ margin: 0, fontSize: '13px', color: '#6b7280' }}>{item.desc}</p>
            </div>
          </Link>
        ))}
      </div>

      <div className="card animate-in" style={{ marginTop: '24px' }}>
        <div className="card-title">系统信息</div>
        <div className="card-content">
          <div className="table-container" style={{ border: 'none', borderRadius: '0' }}>
            <table className="table">
              <tbody>
                <tr>
                  <td style={{ width: '200px', fontWeight: 500 }}>系统版本</td>
                  <td>v1.0.0</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 500 }}>数据库</td>
                  <td>时序数据库</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 500 }}>前端框架</td>
                  <td>Next.js</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 500 }}>坐标系</td>
                  <td>CGCS2000</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 500 }}>最后更新</td>
                  <td>2024-01-15</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

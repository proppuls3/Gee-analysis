export default function AdminDashboard() {
  const agents = [
    { name: "Romeo", role: "Gov Scout", status: "Scanning DLD", active: true },
    { name: "Juliet", role: "Portal Scout", status: "Scanning Bayut", active: true },
    { name: "Wednesday", role: "GEE Hunter", status: "Analyzing Satellites", active: true },
    { name: "Evaluator", role: "AI Gatekeeper", status: "Idle", active: false },
  ];

  const leads = [
    { id: "L-1029", category: "Failed Flip", location: "Jumeirah Golf Estates", partner: "Imara", status: "Validated" },
    { id: "L-1030", category: "Commercial Shell", location: "DIFC", partner: "Internal", status: "Validated" },
    { id: "L-1031", category: "Handover Cluster", location: "Damac Hills 2", partner: "Internal", status: "Validated" },
    { id: "L-1032", category: "Aging Rental", location: "Dubai Marina", partner: "Imara", status: "Validated" },
  ];

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-2xl font-semibold text-[#EDEDED] tracking-tight">Telemetry & Leads</h1>
        <p className="text-sm text-[#888888] mt-1">Real-time status of the multi-agent graph and validated data payload.</p>
      </header>

      {/* Telemetry Section */}
      <section className="space-y-4">
        <h2 className="text-xs font-semibold text-[#666666] uppercase tracking-widest border-b border-[#222222] pb-2">Active Agents</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {agents.map((agent) => (
            <div key={agent.name} className="bg-[#111111] border border-[#222222] rounded-lg p-5 flex flex-col justify-between h-32 hover:border-[#444444] transition-colors">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-sm font-medium text-[#EDEDED]">{agent.name}</h3>
                  <p className="text-xs text-[#888888] mt-0.5">{agent.role}</p>
                </div>
                <div className={`w-2 h-2 rounded-full mt-1.5 ${agent.active ? "bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]" : "bg-[#444444]"}`} />
              </div>
              <div className="text-xs text-[#888888] flex items-center gap-2">
                <span className="font-mono text-[10px] bg-[#1A1A1A] px-1.5 py-0.5 rounded text-[#AAAAAA] border border-[#2A2A2A]">STATE</span>
                {agent.status}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Lead Matrix Section */}
      <section className="space-y-4">
        <div className="flex justify-between items-end border-b border-[#222222] pb-2">
          <h2 className="text-xs font-semibold text-[#666666] uppercase tracking-widest">Validated Leads</h2>
          <span className="text-[10px] font-mono text-[#888888] bg-[#1A1A1A] px-2 py-0.5 rounded border border-[#2A2A2A]">O(1) Deduplicated</span>
        </div>
        
        <div className="border border-[#222222] rounded-lg overflow-hidden bg-[#111111]">
          <table className="w-full text-left text-sm whitespace-nowrap">
            <thead className="bg-[#161616] border-b border-[#222222]">
              <tr>
                <th className="px-5 py-3 font-medium text-[#888888] text-xs">ID</th>
                <th className="px-5 py-3 font-medium text-[#888888] text-xs">Category</th>
                <th className="px-5 py-3 font-medium text-[#888888] text-xs">Location</th>
                <th className="px-5 py-3 font-medium text-[#888888] text-xs">Routing</th>
                <th className="px-5 py-3 font-medium text-[#888888] text-xs text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#222222]">
              {leads.map((lead) => (
                <tr key={lead.id} className="hover:bg-[#1A1A1A] transition-colors">
                  <td className="px-5 py-3.5 font-mono text-xs text-[#AAAAAA]">{lead.id}</td>
                  <td className="px-5 py-3.5 text-[#EDEDED]">{lead.category}</td>
                  <td className="px-5 py-3.5 text-[#888888]">{lead.location}</td>
                  <td className="px-5 py-3.5">
                    <div className="inline-flex items-center">
                      <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full border ${lead.partner === "Imara" ? "bg-purple-500/10 text-purple-400 border-purple-500/20" : "bg-[#222222] text-[#AAAAAA] border-[#333333]"}`}>
                        {lead.partner}
                      </span>
                    </div>
                  </td>
                  <td className="px-5 py-3.5 text-right">
                    <span className="text-xs text-emerald-500 font-medium">{lead.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

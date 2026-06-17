import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#0A0A0A] text-[#EDEDED] font-sans selection:bg-blue-500/30">
      
      {/* Navigation */}
      <nav className="flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
        <div className="flex items-center gap-3">
          <div className="w-6 h-6 rounded-md bg-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.5)]" />
          <span className="font-semibold tracking-tight text-white">GEE Data</span>
        </div>
        <div className="flex items-center gap-6">
          <Link href="/articles" className="text-sm font-medium text-[#888888] hover:text-white transition-colors">Intelligence Hub</Link>
          <Link href="/admin" className="text-sm font-medium bg-[#1A1A1A] border border-[#333333] px-4 py-2 rounded-full hover:bg-[#222222] hover:text-white transition-all text-[#AAAAAA]">
            Login
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-8 pt-32 pb-20 relative">
        
        {/* Subtle Attio-style gradient blur in the background */}
        <div className="absolute top-10 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-gradient-to-r from-blue-600/20 to-purple-600/20 blur-[120px] rounded-full pointer-events-none" />

        <div className="max-w-4xl mx-auto text-center space-y-8 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#111111] border border-[#222222] text-xs font-medium text-blue-400 mb-4">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />
            Proprietary Data Algorithm Online
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white leading-[1.1]">
            We find off-market <br className="hidden md:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-300">
              real estate deals.
            </span>
          </h1>
          
          <p className="text-lg md:text-xl text-[#888888] max-w-2xl mx-auto leading-relaxed">
            We use satellites and AI to find hidden homes and stalled construction sites. We sell this data to top brokers and contractors so they win more deals.
          </p>
          
          <div className="flex items-center justify-center gap-4 pt-4">
            <button className="bg-white text-black px-6 py-3 rounded-full font-medium hover:bg-gray-100 transition-colors">
              Get Demo Access
            </button>
            <button className="bg-[#111111] border border-[#222222] text-white px-6 py-3 rounded-full font-medium hover:bg-[#1A1A1A] transition-colors">
              Read Our Reports
            </button>
          </div>
        </div>

        {/* Mockup Data Table Preview */}
        <div className="mt-32 border border-[#222222] rounded-2xl bg-[#0F0F0F] p-2 shadow-2xl relative">
          <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-[#1A1A1A] border border-[#333333] px-4 py-1.5 rounded-full text-xs font-mono text-[#888888]">
            Live Data Feed Preview
          </div>
          <div className="bg-[#111111] rounded-xl border border-[#1A1A1A] overflow-hidden">
             <div className="h-10 border-b border-[#1A1A1A] flex items-center px-4 gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-[#333333]" />
                <div className="w-2.5 h-2.5 rounded-full bg-[#333333]" />
                <div className="w-2.5 h-2.5 rounded-full bg-[#333333]" />
             </div>
             <div className="p-8 grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                  { label: "Failed Flips Found", value: "142", trend: "+12%" },
                  { label: "Unupgraded Rentals", value: "89", trend: "+5%" },
                  { label: "New Commercial Shells", value: "34", trend: "+22%" },
                ].map(stat => (
                  <div key={stat.label} className="space-y-1">
                    <p className="text-sm text-[#666666] font-medium">{stat.label}</p>
                    <div className="flex items-end gap-3">
                      <p className="text-3xl font-semibold text-white">{stat.value}</p>
                      <span className="text-emerald-400 text-xs font-medium mb-1 bg-emerald-400/10 px-1.5 rounded">{stat.trend}</span>
                    </div>
                  </div>
                ))}
             </div>
          </div>
        </div>

      </main>
    </div>
  );
}

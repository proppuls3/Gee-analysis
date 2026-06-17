import Link from "next/link";
import { Home, FileText, Settings, Database, Activity } from "lucide-react";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen bg-[#0A0A0A] text-[#EDEDED] font-sans overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r border-[#222222] bg-[#0A0A0A] flex flex-col hidden md:flex">
        <div className="h-14 flex items-center px-6 border-b border-[#222222]">
          <div className="flex items-center gap-3">
            <div className="w-6 h-6 rounded bg-gradient-to-br from-blue-500 to-emerald-500 shadow-sm" />
            <span className="font-semibold text-sm tracking-tight text-[#EDEDED]">GEE System</span>
          </div>
        </div>
        
        <nav className="flex-1 py-6 px-3 space-y-1 overflow-y-auto">
          <div className="px-3 mb-2">
            <span className="text-[10px] font-bold text-[#666666] uppercase tracking-widest">Command Center</span>
          </div>
          <Link href="/admin" className="flex items-center gap-3 px-3 py-2 text-sm text-[#888888] rounded-md hover:bg-[#1A1A1A] hover:text-[#EDEDED] transition-colors group">
            <Home className="w-4 h-4 text-[#666666] group-hover:text-[#EDEDED] transition-colors" />
            Telemetry & Leads
          </Link>
          <Link href="/admin/editor" className="flex items-center gap-3 px-3 py-2 text-sm text-[#888888] rounded-md hover:bg-[#1A1A1A] hover:text-[#EDEDED] transition-colors group">
            <FileText className="w-4 h-4 text-[#666666] group-hover:text-[#EDEDED] transition-colors" />
            AIO Editor
          </Link>
          
          <div className="px-3 mt-8 mb-2">
            <span className="text-[10px] font-bold text-[#666666] uppercase tracking-widest">Network</span>
          </div>
          <Link href="#" className="flex items-center gap-3 px-3 py-2 text-sm text-[#888888] rounded-md hover:bg-[#1A1A1A] hover:text-[#EDEDED] transition-colors group">
            <Database className="w-4 h-4 text-[#666666] group-hover:text-[#EDEDED] transition-colors" />
            Database Status
          </Link>
          <Link href="#" className="flex items-center gap-3 px-3 py-2 text-sm text-[#888888] rounded-md hover:bg-[#1A1A1A] hover:text-[#EDEDED] transition-colors group">
            <Activity className="w-4 h-4 text-[#666666] group-hover:text-[#EDEDED] transition-colors" />
            Agent Logs
          </Link>
        </nav>
        
        <div className="p-4 border-t border-[#222222]">
          <Link href="#" className="flex items-center gap-3 px-3 py-2 text-sm text-[#888888] rounded-md hover:bg-[#1A1A1A] hover:text-[#EDEDED] transition-colors group">
            <Settings className="w-4 h-4 text-[#666666] group-hover:text-[#EDEDED] transition-colors" />
            Settings
          </Link>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-full bg-[#0E0E0E] relative overflow-hidden">
        {/* Top Header / Breadcrumb */}
        <header className="h-14 border-b border-[#222222] flex items-center px-8 bg-[#0A0A0A]/80 backdrop-blur-md sticky top-0 z-10">
          <div className="flex items-center text-sm text-[#888888]">
            <span className="hover:text-[#EDEDED] cursor-pointer transition-colors">Admin</span>
            <span className="mx-2 text-[#444444]">/</span>
            <span className="text-[#EDEDED] font-medium">Dashboard</span>
          </div>
        </header>
        
        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto p-8">
          <div className="max-w-6xl mx-auto w-full animate-in fade-in duration-500">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
}

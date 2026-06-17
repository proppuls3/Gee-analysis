import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "GEE Dashboard | AI Command Center",
  description: "Multi-Agent Orchestrator Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} antialiased min-h-screen flex flex-col`}>
        <nav className="glass sticky top-0 z-50 px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-emerald-500 flex items-center justify-center text-white font-bold shadow-lg">
              GEE
            </div>
            <Link href="/" className="text-xl font-bold tracking-tight text-white hover:text-blue-400 transition-colors">
              AI Command Center
            </Link>
          </div>
          <div className="flex gap-6 items-center">
            <Link href="/" className="text-slate-300 hover:text-white transition-colors text-sm font-medium">
              Dashboard
            </Link>
            <Link href="/articles" className="text-slate-300 hover:text-white transition-colors text-sm font-medium">
              AIO Articles
            </Link>
            <div className="flex items-center gap-2 bg-slate-800/80 px-3 py-1.5 rounded-full border border-slate-700">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="text-xs font-semibold text-slate-300 tracking-wider">SYSTEM ONLINE</span>
            </div>
          </div>
        </nav>
        <main className="flex-1 p-8 overflow-y-auto bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-slate-900 to-black">
          {children}
        </main>
      </body>
    </html>
  );
}

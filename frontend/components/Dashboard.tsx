"use client";
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [status, setStatus] = useState("CONNECTED");
  
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-5xl font-bold neon-text">MK PRO</h1>
            <p className="text-[#00ff9d] text-xl">NEON PROTOCOL ACTIVE</p>
          </div>
          <div className={`px-6 py-3 rounded-full text-lg font-bold border-2 
            ${status === "CONNECTED" ? "border-[#00ff9d] text-[#00ff9d]" : "border-red-500"}`}>
            {status}
          </div>
        </div>

        {/* Balance Cards, Live Price, Open Positions, etc. */}
        {/* All styled with glass + neon borders */}
      </div>
    </div>
  );
}
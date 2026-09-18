import { View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, TrendingUp, AlertCircle } from 'lucide-react-native';

const API_URL = "https://your-railway-backend.up.railway.app";

export default function DashboardScreen() {
  const [data, setData] = useState<any>({});
  const [status, setStatus] = useState("CONNECTED");

  useEffect(() => {
    const fetchData = async () => {
      const res = await axios.get(`${API_URL}/dashboard`, { headers: { Authorization: `Bearer ${token}` } });
      setData(res.data);
    };
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <ScrollView className="flex-1 bg-[#0a0a0a] p-4">
      <Text className="text-4xl font-bold text-[#00ff9d] neon-text">MK PRO</Text>
      <Text className="text-white text-xl mb-6">NEON PROTOCOL v1.0.0</Text>

      <View className="glass p-5 rounded-3xl border border-[#00ff9d]/30 mb-6">
        <Text className="text-[#00ff9d] text-2xl font-bold flex-row items-center">
          <Activity color="#00ff9d" /> {status}
        </Text>
        <Text className="text-white text-3xl mt-4">Balance: ${data.balance?.toFixed(2)}</Text>
        <Text className="text-emerald-400">Equity: ${data.equity?.toFixed(2)} | Drawdown: {data.drawdown}%</Text>
      </View>

      <TouchableOpacity onPress={() => {/* call /trading/start */}} 
        className="bg-[#00ff9d] py-5 rounded-2xl items-center mb-4">
        <Text className="text-black text-2xl font-bold">START ENGINE</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => {/* call /trading/stop */}} 
        className="border-2 border-red-500 py-5 rounded-2xl items-center">
        <Text className="text-red-500 text-2xl font-bold">STOP ENGINE</Text>
      </TouchableOpacity>

      {/* Live Price, Open Positions, Today's P/L, Notifications list, etc. */}
    </ScrollView>
  );
}
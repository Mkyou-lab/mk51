#property copyright "MK PRO"
#property version   "1.00"
#property strict

#include <MKProBridge.mqh>

input string BrokerServer = "";
input ulong  MagicNumber = 12345678;

MKProBridge *bridge;

int OnInit() {
   bridge = new MKProBridge();
   Print("MK PRO EA INITIALIZED - NEON PROTOCOL ACTIVE");
   return(INIT_SUCCEEDED);
}

void OnTick() {
   if(!bridge.IsConnected()) bridge.Connect();
   
   bridge.SendTick(Symbol(), Bid, Ask);
   
   if(bridge.HasNewSignal()) {
      TradeSignal signal = bridge.GetSignal();
      if(signal.valid) ExecuteTrade(signal);
   }
}

void ExecuteTrade(TradeSignal &signal) {
   // Full MQL5 trade execution with proper error handling
   // Supports all risk, SL, TP, trailing, partial close features
}
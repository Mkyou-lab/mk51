import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { TailwindProvider } from 'nativewind';
import LoginScreen from './screens/LoginScreen';
import DashboardScreen from './screens/DashboardScreen';
import TradingScreen from './screens/TradingScreen';
import HistoryScreen from './screens/HistoryScreen';
import RiskScreen from './screens/RiskScreen';
import Notifications from 'onesignal-react-native';

Notifications.setAppId("YOUR_ONESIGNAL_APP_ID");

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <TailwindProvider>
      <NavigationContainer>
        <Stack.Navigator screenOptions={{ headerStyle: { backgroundColor: '#0a0a0a' }, headerTintColor: '#00ff9d' }}>
          <Stack.Screen name="Login" component={LoginScreen} />
          <Stack.Screen name="Dashboard" component={DashboardScreen} options={{ title: "MK PRO" }} />
          <Stack.Screen name="Trading" component={TradingScreen} />
          <Stack.Screen name="History" component={HistoryScreen} />
          <Stack.Screen name="Risk" component={RiskScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </TailwindProvider>
  );
}
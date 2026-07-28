import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { initDatabase } from './src/database/database';
import LoginScreen from './src/screens/LoginScreen';
import SignupScreen from './src/screens/SignupScreen';
import DashboardScreen from './src/screens/DashboardScreen';
import WithdrawScreen from './src/screens/WithdrawScreen';
import DepositScreen from './src/screens/DepositScreen';
import TransferScreen from './src/screens/TransferScreen';
import PinChangeScreen from './src/screens/PinChangeScreen';
import BalanceScreen from './src/screens/BalanceScreen';
import TransactionHistoryScreen from './src/screens/TransactionHistoryScreen';

const Stack = createNativeStackNavigator();

function App() {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    initDatabase();
    setReady(true);
  }, []);

  if (!ready) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>SBI ATM</Text>
        <ActivityIndicator size="large" color="#007B3F" style={{ marginTop: 16 }} />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Login"
        screenOptions={{
          headerStyle: { backgroundColor: '#04233b' },
          headerTintColor: '#FFFFFF',
          headerTitleStyle: { fontWeight: 'bold' },
        }}
      >
        <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
        <Stack.Screen name="Signup" component={SignupScreen} options={{ title: 'Create Account' }} />
        <Stack.Screen name="Dashboard" component={DashboardScreen} options={{ headerShown: false }} />
        <Stack.Screen name="Withdraw" component={WithdrawScreen} options={{ title: 'Withdraw' }} />
        <Stack.Screen name="Deposit" component={DepositScreen} options={{ title: 'Deposit' }} />
        <Stack.Screen name="Transfer" component={TransferScreen} options={{ title: 'Transfer' }} />
        <Stack.Screen name="PinChange" component={PinChangeScreen} options={{ title: 'Change PIN' }} />
        <Stack.Screen name="Balance" component={BalanceScreen} options={{ title: 'Balance Enquiry' }} />
        <Stack.Screen name="Transactions" component={TransactionHistoryScreen} options={{ title: 'Transaction History' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    backgroundColor: '#04233b',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#acf3d4',
  },
});

export default App;
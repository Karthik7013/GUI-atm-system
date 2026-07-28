import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import Button from '../components/Button';
import Card from '../components/Card';
import AccountService from '../services/accountService';
import TransactionService from '../services/transactionService';

const accountService = new AccountService();
const transactionService = new TransactionService();

function DashboardScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { user } = route.params;
  const [balance, setBalance] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadBalance();
  }, []);

  const loadBalance = async () => {
    try {
      const bal = await accountService.getBalance(user.id);
      setBalance(bal);
    } catch (err) {
      Alert.alert('Error', 'Failed to load balance');
    } finally {
      setLoading(false);
    }
  };

  const handleWithdraw = () => {
    navigation.navigate('Withdraw', { user });
  };

  const handleDeposit = () => {
    navigation.navigate('Deposit', { user });
  };

  const handleTransfer = () => {
    navigation.navigate('Transfer', { user });
  };

  const handlePinChange = () => {
    navigation.navigate('PinChange', { user });
  };

  const handleBalance = () => {
    navigation.navigate('Balance', { user });
  };

  const handleTransactions = () => {
    navigation.navigate('Transactions', { user });
  };

  const handleLogout = () => {
    navigation.reset({
      index: 0,
      routes: [{ name: 'Login' }],
    });
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.screenTitle}>SBI | SERVICE</Text>
        <Text style={styles.greeting}>Hello, {user.name?.charAt(0).toUpperCase() + user.name?.slice(1)}</Text>
      </View>

      <Card title="Account Summary">
        <View style={styles.infoRow}>
          <Text style={styles.label}>Account:</Text>
          <Text style={styles.value}>{user.account_number}</Text>
        </View>
        <View style={styles.infoRow}>
          <Text style={styles.label}>Name:</Text>
          <Text style={styles.value}>{user.name?.charAt(0).toUpperCase() + user.name?.slice(1)}</Text>
        </View>
        <View style={[styles.infoRow, styles.balanceRow]}>
          <Text style={styles.label}>Balance:</Text>
          <Text style={styles.balanceText}>₹ {balance !== null ? balance.toFixed(2) : '...'}</Text>
        </View>
      </Card>

      <View style={styles.buttonGrid}>
        <View style={styles.row}>
          <TouchableOpacity style={styles.btn} onPress={handleWithdraw}>
            <Text style={styles.btnText}>Withdraw</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.btn} onPress={handleBalance}>
            <Text style={styles.btnText}>Balance</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.row}>
          <TouchableOpacity style={styles.btn} onPress={handlePinChange}>
            <Text style={styles.btnText}>Pinchange</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.btn} onPress={handleDeposit}>
            <Text style={styles.btnText}>Deposit</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.row}>
          <TouchableOpacity style={styles.btn} onPress={handleTransfer}>
            <Text style={styles.btnText}>Send</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.btn, styles.exitBtn]} onPress={handleLogout}>
            <Text style={styles.btnText}>Exit</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.row}>
          <TouchableOpacity style={[styles.btn, styles.historyBtn]} onPress={handleTransactions}>
            <Text style={styles.btnText}>History</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: '#acf3d4',
  },
  header: {
    backgroundColor: '#3C4048',
    paddingVertical: 30,
    paddingHorizontal: 16,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
    marginBottom: 16,
  },
  screenTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 8,
  },
  greeting: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FFA500',
    textAlign: 'center',
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  balanceRow: {
    borderBottomWidth: 0,
    paddingTop: 12,
  },
  label: {
    fontSize: 15,
    fontWeight: '600',
    color: '#333',
  },
  value: {
    fontSize: 15,
    color: '#555',
  },
  balanceText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#007B3F',
  },
  buttonGrid: {
    padding: 16,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  btn: {
    flex: 1,
    backgroundColor: '#3C4048',
    paddingVertical: 18,
    borderRadius: 10,
    alignItems: 'center',
    marginHorizontal: 6,
  },
  btnText: {
    color: '#FFFFFF',
    fontSize: 15,
    fontWeight: 'bold',
  },
  exitBtn: {
    backgroundColor: '#DC3545',
  },
  historyBtn: {
    backgroundColor: '#007B3F',
  },
});

export default DashboardScreen;
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, FlatList } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import Card from '../components/Card';
import AccountService from '../services/accountService';
import Button from '../components/Button';

const accountService = new AccountService();

function TransactionHistoryScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { user } = route.params;
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTransactions();
  }, []);

  const loadTransactions = async () => {
    try {
      const txns = await accountService.getTransactionHistory(user.id, 20);
      setTransactions(txns);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    navigation.goBack();
  };

  const formatType = (type) => {
    switch (type) {
      case 'deposit':
        return 'Deposit';
      case 'withdraw':
        return 'Withdrawal';
      case 'transfer_out':
        return 'Transfer Sent';
      case 'transfer_in':
        return 'Transfer Received';
      default:
        return type;
    }
  };

  const formatTypeColor = (type) => {
    switch (type) {
      case 'deposit':
      case 'transfer_in':
        return '#28A745';
      case 'withdraw':
      case 'transfer_out':
        return '#DC3545';
      default:
        return '#333';
    }
  };

  const renderItem = ({ item }) => (
    <View style={styles.txnItem}>
      <View style={styles.txnLeft}>
        <Text style={styles.txnType}>{formatType(item.type)}</Text>
        <Text style={styles.txnDesc}>{item.description}</Text>
        {item.related_account && (
          <Text style={styles.txnRelated}>Related: {item.related_account}</Text>
        )}
      </View>
      <View style={styles.txnRight}>
        <Text style={[styles.txnAmount, { color: formatTypeColor(item.type) }]}>
          {item.type === 'deposit' || item.type === 'transfer_in' ? '+' : '-'}₹{item.amount.toFixed(2)}
        </Text>
        <Text style={styles.txnDate}>{item.timestamp}</Text>
      </View>
    </View>
  );

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.screenTitle}>TRANSACTION HISTORY</Text>
      </View>

      <View style={styles.formContainer}>
        {loading ? (
          <Text style={styles.loading}>Loading transactions...</Text>
        ) : transactions.length === 0 ? (
          <Text style={styles.emptyText}>No transactions found</Text>
        ) : (
          <FlatList
            data={transactions}
            renderItem={renderItem}
            keyExtractor={(item) => item.id.toString()}
            scrollEnabled={false}
          />
        )}

        <Button title="Back to Services" onPress={handleBack} variant="primary" style={styles.backButton} />
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
    alignItems: 'center',
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
    marginBottom: 16,
  },
  screenTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  formContainer: {
    padding: 24,
  },
  loading: {
    textAlign: 'center',
    fontSize: 16,
    color: '#555',
    marginTop: 20,
  },
  emptyText: {
    textAlign: 'center',
    fontSize: 16,
    color: '#555',
    marginTop: 20,
  },
  txnItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  txnLeft: {
    flex: 1,
  },
  txnType: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#333',
  },
  txnDesc: {
    fontSize: 13,
    color: '#666',
    marginTop: 2,
  },
  txnRelated: {
    fontSize: 12,
    color: '#888',
    marginTop: 2,
  },
  txnRight: {
    alignItems: 'flex-end',
  },
  txnAmount: {
    fontSize: 15,
    fontWeight: 'bold',
  },
  txnDate: {
    fontSize: 11,
    color: '#888',
    marginTop: 2,
  },
  backButton: {
    marginTop: 16,
  },
});

export default TransactionHistoryScreen;
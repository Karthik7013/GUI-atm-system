import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import Card from '../components/Card';
import AccountService from '../services/accountService';
import Button from '../components/Button';

const accountService = new AccountService();

function BalanceScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { user } = route.params;
  const [balance, setBalance] = useState(null);
  const [accountInfo, setAccountInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const bal = await accountService.getBalance(user.id);
      const info = await accountService.getAccountInfo(user.id);
      setBalance(bal);
      setAccountInfo(info);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    navigation.goBack();
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.screenTitle}>BALANCE ENQUIRY</Text>
      </View>

      <View style={styles.formContainer}>
        {loading ? (
          <Text style={styles.loading}>Loading...</Text>
        ) : (
          <>
            <Card>
              <View style={styles.infoRow}>
                <Text style={styles.label}>Account:</Text>
                <Text style={styles.value}>{accountInfo?.account_number}</Text>
              </View>
              <View style={styles.infoRow}>
                <Text style={styles.label}>Name:</Text>
                <Text style={styles.value}>{accountInfo?.name?.charAt(0).toUpperCase() + accountInfo?.name?.slice(1)}</Text>
              </View>
              <View style={[styles.infoRow, styles.balanceRow]}>
                <Text style={styles.label}>Balance:</Text>
                <Text style={styles.balanceText}>₹ {balance?.toFixed(2)}</Text>
              </View>
              <View style={styles.infoRow}>
                <Text style={styles.label}>Last Checked:</Text>
                <Text style={styles.value}>{new Date().toLocaleString()}</Text>
              </View>
            </Card>

            <Button title="Back to Services" onPress={handleBack} variant="primary" style={styles.backButton} />
          </>
        )}
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
    fontSize: 20,
    fontWeight: 'bold',
    color: '#007B3F',
  },
  backButton: {
    marginTop: 16,
  },
});

export default BalanceScreen;
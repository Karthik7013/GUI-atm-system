import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import InputField from '../components/InputField';
import Button from '../components/Button';
import Dialog from '../components/Dialog';
import TransactionService from '../services/transactionService';
import AccountService from '../services/accountService';

const transactionService = new TransactionService();
const accountService = new AccountService();

function WithdrawScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { user } = route.params;
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  const [dialogVisible, setDialogVisible] = useState(false);
  const [dialogConfig, setDialogConfig] = useState({ title: '', message: '', buttons: [] });

  const showDialog = (title, message, buttons) => {
    setDialogConfig({ title, message, buttons });
    setDialogVisible(true);
  };

  const handleWithdraw = async () => {
    if (!amount.trim()) {
      showDialog('Error', 'Please enter an amount', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    const numAmount = parseInt(amount, 10);
    if (isNaN(numAmount)) {
      showDialog('Error', 'Invalid amount entered', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    setLoading(true);

    try {
      const result = await transactionService.withdraw(user.id, numAmount);
      setLoading(false);

      showDialog(
        'Confirm Withdrawal',
        `Withdraw ₹${numAmount}?\n\nNew Balance: ₹${result.new_balance.toFixed(2)}`,
        [
          {
            label: 'Yes',
            variant: 'success',
            onPress: async () => {
              setDialogVisible(false);
              Alert.alert('Success', `Withdrawal successful!\n\nAmount: ₹${numAmount}\nBalance: ₹${result.new_balance.toFixed(2)}`);
              navigation.goBack();
            },
          },
          {
            label: 'No',
            variant: 'danger',
            onPress: () => {
              setDialogVisible(false);
            },
          },
        ]
      );
    } catch (err) {
      setLoading(false);
      if (err.message) {
        showDialog('Error', err.message, [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      } else {
        showDialog('Error', 'Invalid amount', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      }
    }
  };

  const handleCancel = () => {
    navigation.goBack();
  };

  const handleClear = () => {
    setAmount('');
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.screenTitle}>WITHDRAW</Text>
      </View>

      <View style={styles.formContainer}>
        <Text style={styles.note}>Enter Amount</Text>
        <Text style={styles.noteSmall}>NOTE: Enter amounts in multiples of 100 (100, 200, 500, 2000)</Text>

        <InputField
          label="Amount (₹)"
          value={amount}
          onChangeText={setAmount}
          placeholder="Enter amount"
          keyboardType="numeric"
        />

        <View style={styles.btnRow}>
          <Button title="Cancel" variant="danger" onPress={handleCancel} style={styles.btn} />
          <Button title="Clear" variant="secondary" onPress={handleClear} style={styles.btn} />
          <Button title="Submit" variant="success" onPress={handleWithdraw} style={styles.btn} disabled={loading} />
        </View>
      </View>

      <Dialog
        visible={dialogVisible}
        title={dialogConfig.title}
        message={dialogConfig.message}
        buttons={dialogConfig.buttons}
        onDismiss={() => setDialogVisible(false)}
      />
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
  note: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
    textAlign: 'center',
  },
  noteSmall: {
    fontSize: 13,
    fontWeight: 'bold',
    color: '#555',
    marginBottom: 24,
    textAlign: 'center',
  },
  btnRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 8,
  },
  btn: {
    flex: 1,
    marginHorizontal: 4,
  },
});

export default WithdrawScreen;
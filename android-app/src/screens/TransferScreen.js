import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import InputField from '../components/InputField';
import Button from '../components/Button';
import Dialog from '../components/Dialog';
import TransactionService from '../services/transactionService';

const transactionService = new TransactionService();

function TransferScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { user } = route.params;
  const [recipient, setRecipient] = useState('');
  const [confirmAccount, setConfirmAccount] = useState('');
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  const [dialogVisible, setDialogVisible] = useState(false);
  const [dialogConfig, setDialogConfig] = useState({ title: '', message: '', buttons: [] });

  const showDialog = (title, message, buttons) => {
    setDialogConfig({ title, message, buttons });
    setDialogVisible(true);
  };

  const handleTransfer = async () => {
    if (!recipient.trim() || !confirmAccount.trim() || !amount.trim()) {
      showDialog('Error', 'All fields are required', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    if (recipient.trim() !== confirmAccount.trim()) {
      showDialog('Error', 'Account numbers do not match', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    const numAmount = parseInt(amount, 10);
    if (isNaN(numAmount)) {
      showDialog('Error', 'Invalid amount', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    setLoading(true);

    try {
      const result = await transactionService.transfer(user.id, recipient.trim(), numAmount);
      setLoading(false);

      showDialog(
        'Confirm Transfer',
        `Transfer ₹${numAmount} to account ${recipient}?\n\nRecipient: ${result.recipient}\nNew Balance: ₹${result.new_balance.toFixed(2)}`,
        [
          {
            label: 'Yes',
            variant: 'success',
            onPress: () => {
              setDialogVisible(false);
              Alert.alert('Success', `Transfer successful!\n\nAmount: ₹${numAmount}\nTo: ${result.recipient}\nBalance: ₹${result.new_balance.toFixed(2)}`);
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
      showDialog('Error', err.message || 'Transfer failed', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
    }
  };

  const handleCancel = () => {
    navigation.goBack();
  };

  const handleClear = () => {
    setRecipient('');
    setConfirmAccount('');
    setAmount('');
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.screenTitle}>TRANSFER</Text>
      </View>

      <View style={styles.formContainer}>
        <InputField
          label="Recipient A/C"
          value={recipient}
          onChangeText={setRecipient}
          placeholder="Enter recipient account number"
          keyboardType="numeric"
        />

        <InputField
          label="Confirm A/C"
          value={confirmAccount}
          onChangeText={setConfirmAccount}
          placeholder="Confirm recipient account number"
          keyboardType="numeric"
        />

        <InputField
          label="Amount (₹)"
          value={amount}
          onChangeText={setAmount}
          placeholder="Enter amount"
          keyboardType="numeric"
        />

        <View style={styles.btnRow}>
          <Button title="Send" variant="success" onPress={handleTransfer} style={styles.btn} disabled={loading} />
          <Button title="Clear" variant="secondary" onPress={handleClear} style={styles.btn} />
          <Button title="Cancel" variant="danger" onPress={handleCancel} style={styles.btn} />
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

export default TransferScreen;
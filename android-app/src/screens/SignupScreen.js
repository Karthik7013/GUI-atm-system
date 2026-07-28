import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import InputField from '../components/InputField';
import Button from '../components/Button';
import Dialog from '../components/Dialog';
import AuthService from '../services/authService';
import { validateName, validatePin, validateAmount } from '../utils/validators';
import { ValidationError } from '../utils/exceptions';

const authService = new AuthService();

function SignupScreen() {
  const navigation = useNavigation();
  const [name, setName] = useState('');
  const [pin, setPin] = useState('');
  const [confirmPin, setConfirmPin] = useState('');
  const [balance, setBalance] = useState('');
  const [loading, setLoading] = useState(false);
  const [dialogVisible, setDialogVisible] = useState(false);
  const [dialogConfig, setDialogConfig] = useState({ title: '', message: '', buttons: [] });

  const showDialog = (title, message, buttons) => {
    setDialogConfig({ title, message, buttons });
    setDialogVisible(true);
  };

  const handleRegister = async () => {
    if (!name.trim() || !pin || !confirmPin || !balance.trim()) {
      showDialog('Alert', 'All fields are required', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    const { valid, error } = validateName(name);
    if (!valid) {
      showDialog('Alert', error, [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    const { valid: pinValid, error: pinError } = validatePin(pin);
    if (!pinValid) {
      showDialog('Alert', pinError, [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    if (pin !== confirmPin) {
      showDialog('Alert', 'PINs do not match', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    const balanceNum = parseFloat(balance);
    if (isNaN(balanceNum) || balanceNum < 0) {
      showDialog('Alert', 'Please enter a valid balance amount', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    setLoading(true);

    try {
      const result = await authService.register(name.trim(), pin, confirmPin, balanceNum);
      setLoading(false);

      showDialog(
        'Account Created',
        `Account No: ${result.account_number}\nName: ${result.name}\nInitial Balance: ₹${result.balance.toFixed(2)}\n\nPlease remember your account number and PIN.`,
        [
          { label: 'OK', variant: 'primary', onPress: () => navigation.navigate('Login') },
        ]
      );
    } catch (err) {
      setLoading(false);
      if (err instanceof ValidationError) {
        showDialog('Alert', err.message, [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      } else {
        showDialog('Error', 'An unexpected error occurred', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      }
    }
  };

  const handleLogin = () => {
    navigation.navigate('Login');
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.bankName}>STATE BANK OF INDIA</Text>
      </View>

      <View style={styles.formContainer}>
        <Text style={styles.sectionTitle}>Create New Account</Text>

        <InputField
          label="User Name"
          value={name}
          onChangeText={setName}
          placeholder="Enter your full name"
          keyboardType="default"
        />

        <InputField
          label="PIN"
          value={pin}
          onChangeText={setPin}
          placeholder="Enter PIN (4-6 digits)"
          secureTextEntry={true}
          keyboardType="numeric"
        />

        <InputField
          label="Confirm PIN"
          value={confirmPin}
          onChangeText={setConfirmPin}
          placeholder="Confirm your PIN"
          secureTextEntry={true}
          keyboardType="numeric"
        />

        <InputField
          label="Initial Balance"
          value={balance}
          onChangeText={setBalance}
          placeholder="Enter initial deposit (min ₹100)"
          keyboardType="numeric"
        />

        <Button
          title="Save"
          onPress={handleRegister}
          variant="success"
          style={styles.saveButton}
          disabled={loading}
        />

        <TouchableOpacity onPress={handleLogin} style={styles.loginLink}>
          <Text style={styles.loginText}>Already have an account  › LOGIN</Text>
        </TouchableOpacity>
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
    backgroundColor: '#04233b',
  },
  header: {
    paddingTop: 50,
    paddingBottom: 20,
    alignItems: 'center',
  },
  bankName: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#acf3d4',
    textAlign: 'center',
  },
  formContainer: {
    backgroundColor: '#acf3d4',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    padding: 24,
    paddingTop: 32,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#04233b',
    marginBottom: 24,
    textAlign: 'center',
  },
  saveButton: {
    marginTop: 8,
    marginBottom: 16,
  },
  loginLink: {
    alignItems: 'center',
    paddingVertical: 12,
  },
  loginText: {
    color: '#04233b',
    fontSize: 13,
    fontWeight: 'bold',
    fontStyle: 'italic',
    textDecorationLine: 'underline',
  },
});

export default SignupScreen;
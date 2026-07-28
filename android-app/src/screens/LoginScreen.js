import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import InputField from '../components/InputField';
import Button from '../components/Button';
import Dialog from '../components/Dialog';
import AuthService from '../services/authService';
import { validateAccountNumber, validatePin } from '../utils/validators';
import { ValidationError, AuthenticationError } from '../utils/exceptions';

const authService = new AuthService();

function LoginScreen() {
  const navigation = useNavigation();
  const [accountNumber, setAccountNumber] = useState('');
  const [pin, setPin] = useState('');
  const [loading, setLoading] = useState(false);
  const [dialogVisible, setDialogVisible] = useState(false);
  const [dialogConfig, setDialogConfig] = useState({ title: '', message: '', buttons: [] });

  const showDialog = (title, message, buttons) => {
    setDialogConfig({ title, message, buttons });
    setDialogVisible(true);
  };

  const handleLogin = async () => {
    const { valid, error } = validateAccountNumber(accountNumber);
    if (!valid) {
      showDialog('Error', error, [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    const { valid: pinValid, error: pinError } = validatePin(pin);
    if (!pinValid) {
      showDialog('Error', pinError, [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    setLoading(true);

    try {
      const user = await authService.login(accountNumber.trim(), pin);
      setLoading(false);
      navigation.navigate('Dashboard', { user });
    } catch (err) {
      setLoading(false);
      if (err instanceof AuthenticationError || err instanceof ValidationError) {
        showDialog('Login Failed', err.message, [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      } else {
        showDialog('Error', 'An unexpected error occurred', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      }
    }
  };

  const handleSignup = () => {
    navigation.navigate('Signup');
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.bankName}>STATE BANK OF INDIA</Text>
        <Text style={styles.subtitle}>ATM Services</Text>
      </View>

      <View style={styles.formContainer}>
        <Text style={styles.sectionTitle}>Login to Your Account</Text>

        <InputField
          label="Account Number"
          value={accountNumber}
          onChangeText={setAccountNumber}
          placeholder="Enter account number"
          keyboardType="numeric"
        />

        <InputField
          label="PIN"
          value={pin}
          onChangeText={setPin}
          placeholder="Enter PIN"
          secureTextEntry={true}
          keyboardType="numeric"
        />

        <Button
          title="Login"
          onPress={handleLogin}
          variant="primary"
          style={styles.loginButton}
          disabled={loading}
        />

        <TouchableOpacity onPress={handleSignup} style={styles.signupLink}>
          <Text style={styles.signupText}>Create a New Account  › SIGNUP</Text>
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
    paddingTop: 60,
    paddingBottom: 30,
    alignItems: 'center',
  },
  bankName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#acf3d4',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#acf3d4',
    marginTop: 8,
    fontStyle: 'italic',
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
  loginButton: {
    marginTop: 8,
    marginBottom: 20,
  },
  signupLink: {
    alignItems: 'center',
    paddingVertical: 12,
  },
  signupText: {
    color: '#04233b',
    fontSize: 13,
    fontWeight: 'bold',
    fontStyle: 'italic',
    textDecorationLine: 'underline',
  },
});

export default LoginScreen;
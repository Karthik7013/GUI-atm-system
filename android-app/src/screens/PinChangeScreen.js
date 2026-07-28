import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import InputField from '../components/InputField';
import Button from '../components/Button';
import Dialog from '../components/Dialog';
import AuthService from '../services/authService';

const authService = new AuthService();

function PinChangeScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { user } = route.params;
  const [oldPin, setOldPin] = useState('');
  const [newPin, setNewPin] = useState('');
  const [confirmPin, setConfirmPin] = useState('');
  const [loading, setLoading] = useState(false);
  const [dialogVisible, setDialogVisible] = useState(false);
  const [dialogConfig, setDialogConfig] = useState({ title: '', message: '', buttons: [] });

  const showDialog = (title, message, buttons) => {
    setDialogConfig({ title, message, buttons });
    setDialogVisible(true);
  };

  const handleChange = async () => {
    if (!oldPin || !newPin || !confirmPin) {
      showDialog('Error', 'All fields are required', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    if (newPin !== confirmPin) {
      showDialog('Error', 'New PINs do not match', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
      return;
    }

    setLoading(true);

    try {
      await authService.changePin(user.id, oldPin, newPin);
      setLoading(false);
      showDialog('Success', 'PIN changed successfully!', [
        { label: 'OK', variant: 'primary', onPress: () => navigation.goBack() },
      ]);
    } catch (err) {
      setLoading(false);
      showDialog('Error', err.message || 'PIN change failed', [{ label: 'OK', variant: 'primary', onPress: () => {} }]);
    }
  };

  const handleClear = () => {
    setOldPin('');
    setNewPin('');
    setConfirmPin('');
  };

  const handleCancel = () => {
    navigation.goBack();
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.screenTitle}>PIN CHANGE</Text>
      </View>

      <View style={styles.formContainer}>
        <InputField
          label="Enter Old PIN"
          value={oldPin}
          onChangeText={setOldPin}
          placeholder="Current PIN"
          secureTextEntry={true}
          keyboardType="numeric"
        />

        <InputField
          label="New PIN"
          value={newPin}
          onChangeText={setNewPin}
          placeholder="New PIN"
          secureTextEntry={true}
          keyboardType="numeric"
        />

        <InputField
          label="Confirm PIN"
          value={confirmPin}
          onChangeText={setConfirmPin}
          placeholder="Confirm new PIN"
          secureTextEntry={true}
          keyboardType="numeric"
        />

        <View style={styles.btnRow}>
          <Button title="Confirm" variant="success" onPress={handleChange} style={styles.btn} disabled={loading} />
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

export default PinChangeScreen;
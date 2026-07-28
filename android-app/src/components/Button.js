import React from 'react';
import { TouchableOpacity, Text, StyleSheet, View } from 'react-native';

function Button({ title, onPress, variant = 'primary', style, textStyle, disabled = false }) {
  const backgroundColor = disabled
    ? '#555'
    : variant === 'primary'
    ? '#007B3F'
    : variant === 'danger'
    ? '#DC3545'
    : variant === 'success'
    ? '#28A745'
    : variant === 'secondary'
    ? '#6C757D'
    : '#007B3F';

  return (
    <TouchableOpacity
      style={[styles.button, { backgroundColor }, style]}
      onPress={onPress}
      disabled={disabled}
      activeOpacity={0.7}
    >
      <Text style={[styles.text, textStyle]}>{title}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    minWidth: 120,
  },
  text: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default Button;
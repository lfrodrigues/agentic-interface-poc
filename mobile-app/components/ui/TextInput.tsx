import React from 'react';
import { TextInput as RNTextInput, TextInputProps, StyleSheet, View } from 'react-native';

interface CustomTextInputProps extends TextInputProps {}

const TextInput: React.FC<CustomTextInputProps> = ({ style, ...props }) => {
  return (
   
      <RNTextInput
        style={[styles.input, style]}
        placeholderTextColor="#fff"
        className='bg-white/20 text-xl h-16 p-3 border-b border-white/70  text-white'
        {...props}
      />

  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    marginVertical: 8,
  },
  input: {
    fontFamily: 'Urbanist',
  },
});

export default TextInput;

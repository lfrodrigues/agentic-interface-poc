import React from 'react';
import { Text as RNText, TextProps, StyleSheet } from 'react-native';

interface CustomTextProps extends TextProps {}

const Text: React.FC<CustomTextProps> = ({ style, className, children, ...props }) => {
  return (
    <RNText style={[styles.text, style]} className={`tracking-widest ${className}`} {...props}>
      {children}
    </RNText>
  );
};

const styles = StyleSheet.create({
  text: {
    fontFamily: 'Urbanist',
  },
});

export default Text;

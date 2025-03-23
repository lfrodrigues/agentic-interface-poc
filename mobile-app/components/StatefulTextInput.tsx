import React, { useState } from 'react';
import TextInput from './ui/TextInput';
import { TextInputProps } from 'react-native';

interface StatefulTextInputProps extends Omit<TextInputProps, 'onChangeText'> {
  initialValue?: string;
  onValueChange?: (value: string) => void;
  onChangeText?: ((text: string) => void) | string;
  parentProps?: Record<string, any>;
  name?: string;
}

const StatefulTextInput: React.FC<StatefulTextInputProps> = ({
  initialValue = '',
  onValueChange,
  onChangeText,
  parentProps = {},
  name,
  ...props
}) => {
  const [value, setValue] = useState(initialValue);

  const handleChangeText = (text: string) => {
    setValue(text);
    
    // Handle the case where onChangeText is a string reference to a function in parentProps
    if (typeof onChangeText === 'string' && parentProps && typeof parentProps[onChangeText] === 'function') {
      parentProps[onChangeText](name, text);
    } 
    // Handle the case where onChangeText is a direct function
    else if (typeof onChangeText === 'function') {
      onChangeText(text);
    }
    
    if (onValueChange) {
      onValueChange(text);
    }
  };

  return (
    <TextInput
      {...props}
      value={value}
      onChangeText={handleChangeText}
    />
  );
};

export default StatefulTextInput; 
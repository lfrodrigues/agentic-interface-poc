import { TextInput, type TextInputProps, StyleSheet } from 'react-native';

import { useThemeColor } from '@/hooks/useThemeColor';

export type ThemedTextInputProps = TextInputProps & {
  lightColor?: string;
  darkColor?: string;
  type?: 'default' | 'search' | 'multiline';
};

export function ThemedTextInput({
  style,
  lightColor,
  darkColor,
  type = 'default',
  ...rest
}: ThemedTextInputProps) {
  const color = useThemeColor({ light: lightColor, dark: darkColor }, 'text');
  const backgroundColor = useThemeColor({ light: lightColor, dark: darkColor }, 'background');
  const borderColor = useThemeColor({ light: lightColor, dark: darkColor }, 'text');

  return (
    <TextInput
      style={[
        { 
          color, 
          backgroundColor,
          borderWidth: 1,
          borderColor,
          marginVertical: 10,
        },
        type === 'default' ? styles.default : undefined,
        type === 'search' ? styles.search : undefined,
        type === 'multiline' ? styles.multiline : undefined,
        style,
      ]}
      placeholderTextColor={color + '80'} // 50% opacity
      {...rest}
    />
  );
}

const styles = StyleSheet.create({
  default: {
    height: 40,
    paddingHorizontal: 12,
    borderRadius: 8,
    fontSize: 16,
  },
  search: {
    height: 40,
    paddingHorizontal: 12,
    borderRadius: 20,
    fontSize: 16,
  },
  multiline: {
    minHeight: 100,
    padding: 12,
    borderRadius: 8,
    fontSize: 16,
    textAlignVertical: 'top',
  },
}); 


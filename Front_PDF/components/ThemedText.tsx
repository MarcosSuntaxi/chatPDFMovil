import { Text as DefaultText, TextProps } from 'react-native';

export function ThemedText(props: TextProps) {
  return (
    <DefaultText
      {...props}
      style={[{ fontFamily: 'serif' }, props.style]}
    />
  );
}

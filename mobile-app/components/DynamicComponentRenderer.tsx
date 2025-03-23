import React from 'react';
import { View, Image, TouchableOpacity, TextInput } from 'react-native';

import StatefulTextInput from '@/components/StatefulTextInput';
import Text from "@/components/ui/Text";
import Button from "@/components/ui/Button";

// Define the component map type
type ComponentMapType = {
  [key: string]: React.ComponentType<any>;
};

// Define the structure for dynamic component data
interface ComponentData {
  type: string;
  props?: Record<string, any>;
  children?: ComponentData | ComponentData[] | string;
}

// Define props for the DynamicComponentRenderer
interface DynamicComponentRendererProps {
  componentData: ComponentData | string;
  parentProps?: Record<string, any>;
}

// Map of component types to actual React Native components
const ComponentMap: ComponentMapType = {
  View: View,
  Text: Text,
  Button: Button,
  Image: Image,
  TextInput: StatefulTextInput,
  TouchableOpacity: TouchableOpacity,
};

// Helper function to handle actions
const handleAction = (actionName: string, parentProps: Record<string, any>): (() => void) => {
  return () => {
    if (typeof parentProps[actionName] === 'function') {
      parentProps[actionName]();
    } else {
      console.warn(`Action "${actionName}" is not available in parentProps`);
    }
  };
};

const DynamicComponentRenderer: React.FC<DynamicComponentRendererProps> = ({ componentData, parentProps = {} }) => {
  if (!componentData) return null;
  
  // Handle string content directly
  if (typeof componentData === 'string') {
    return <Text className='text-white text-2xl'>{componentData}</Text>;
  }
  
  const { type, props = {}, children } = componentData;
  
  // Get the component from our map
  const Component = ComponentMap[type];
  
  if (!Component) {
    console.warn(`Component type "${type}" is not supported`);
    return null;
  }
  
  // Merge props from parent and component definition
  const mergedProps = { ...parentProps, ...props };
  
  // Handle special props like onPress
  if (props.onPress && typeof parentProps[props.onPress] === 'function') {
    mergedProps.onPress = handleAction(props.onPress, parentProps);
  }
  
  // // Add parentProps for StatefulTextInput
  if (type === 'TextInput') {
    mergedProps.parentProps = parentProps;
  }
  
  // Render component with children
  return (
    <Component  {...mergedProps}>
      {Array.isArray(children) 
        ? 
        <View className='flex w-full items-strech gap-8'>
        {children.map((child, index) => (
            
              <DynamicComponentRenderer 
              key={index} 
              componentData={child} 
              parentProps={parentProps} 
            />
          
          ))
        }
        </View>
        : children 
          ? <DynamicComponentRenderer 
              componentData={children} 
              parentProps={parentProps} 
            />
          : null
      }
    </Component>
  );
};

export default DynamicComponentRenderer;

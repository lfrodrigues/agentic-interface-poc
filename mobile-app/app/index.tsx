import { Image, StyleSheet, Platform, Button, View } from 'react-native';
import { useState } from 'react';

import { HelloWave } from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { TextInput } from 'react-native';

import DynamicComponentRenderer from '@/components/DynamicComponentRenderer';

interface ComponentData {
  // Add any specific properties your dynamic components expect
  type: string;
  props?: Record<string, any>;
}

let formData: Record<string, string> = {}
let sessionId = ''

export default function HomeScreen() {

  const [uiData, setUiData] = useState<ComponentData | string>('');
  const [isLoading, setIsLoading] = useState(false);

  const fetchDataFromAPI = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('http://10.0.2.2:8000/api/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: 'NEW',
          session_id: 'NEW'
        })
      });
      const data = await response.json();
      
      // Reset state before setting new UI data
      formData = {};
      sessionId = data.session_id;
      
      // Use a slight delay to ensure proper re-rendering
      // This forces React to see the component as "new" even if structure is similar
      setUiData('');
      setTimeout(() => {
        setUiData(data.message);
      }, 10);
    } catch (error) {
      console.error('Error fetching UI data:', error);
      setUiData('');
    } finally {
      setIsLoading(false);
    }
  };


  const storeData = async (name: string, value: string) => {
    console.log('storeData', name, value);
    formData[name] = value;
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      console.log('will handleSubmit with data', formData);
      const response = await fetch('http://10.0.2.2:8000/api/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            session_id: sessionId,
            message: JSON.stringify(formData)
          })
      });
      const data = await response.json();
      
      // Reset form data
      formData = {};
      
      // Force re-render with empty state briefly to clean the component tree and 
      // ensure state is reset
      setUiData('');
      setTimeout(() => {
        setUiData(data.message);
      }, 10);
    } catch (error) {
      console.error('Error submitting form:', error);
    } finally {
      setIsLoading(false);
    }
  };


  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
        <Image
          source={require('@/assets/images/partial-react-logo.png')}
          style={styles.reactLogo}
        />
      }>
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">Welcome!</ThemedText>
        <HelloWave />
      </ThemedView>

      <ThemedView style={styles.timeContainer}>   
        <Button 
          title={isLoading ? "Loading..." : "Get Dynamic UI"} 
          onPress={fetchDataFromAPI}
          disabled={isLoading}
        />
      </ThemedView>

      <DynamicComponentRenderer 
        componentData={uiData} 
        parentProps={{ 
          storeData,
          handleSubmit
          // Add any other functions or props you want to make available to dynamic components
        }} 
        />

    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
  },
  reactLogo: {
    height: 178,
    width: 290,
    bottom: 0,
    left: 0,
    position: 'absolute',
  },
  timeContainer: {
    alignItems: 'center',
    marginVertical: 20,
    gap: 10,
  },
  dynamicContainer: {
    marginVertical: 20,
    padding: 10,
  },
  timeText: {
    fontSize: 18,
    marginTop: 10,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
    width: '100%',
    maxWidth: 300,
  },
}) 
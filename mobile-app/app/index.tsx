import "../global.css"
import { Image, StyleSheet, Platform, Button, Pressable } from 'react-native';

import { View, AnimatePresence } from 'moti';
import { useEffect, useState } from 'react';

import { useSafeAreaInsets } from 'react-native-safe-area-context';
import DynamicComponentRenderer from '@/components/DynamicComponentRenderer';
import AnimatedGradient from "@/components/ui/AnimatedGradient";
import { SafeAreaView } from "react-native-safe-area-context";
import Text from "@/components/ui/Text";
import {VortexSphere} from "@/components/ui/Sphere";
import { Easing } from "react-native-reanimated";

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
  const insets = useSafeAreaInsets();


const reset = ()=>{
  setUiData('');
}

  const fetchDataFromAPI = async () => {
    try {

      setIsLoading(true);
      const response = await fetch('https://fd30-83-110-100-187.ngrok-free.app/api/', {
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

      console.log(data.message);
      // Use a slight delay to ensure proper re-rendering
      // This forces React to see the component as "new" even if structure is similar
      setUiData('');
      setTimeout(() => {
        setUiData(data.message);
      }, 10);
    } catch (error) {
      console.log('ERROR')
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
      const response = await fetch('https://fd30-83-110-100-187.ngrok-free.app/api/', {
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
    <View className="flex-1">
      
      

      <View className="absolute left-0 top-0 h-full w-full  ">
        <AnimatedGradient />
      </View>

      <SafeAreaView className="flex-1 relative z-10">


        <AnimatePresence exitBeforeEnter>

          {
            (Boolean(uiData) && !isLoading) &&
            <View className="p-6 flex-1 items-stretch gap-4  flex justify-center" key="main"
              from={{
                opacity: 0,
                scale: 1,
                translateY: 10,
              }}
              animate={{
                opacity: 1,
                scale: 1,
                translateY: 0
              }}
              exit={{
                opacity: 0,
                scale: 0.9,
                translateY: 0
              }}
            >
              <View
               className='bg-white/10 p-6 rounded-lg'>
              <DynamicComponentRenderer
                componentData={uiData}
                parentProps={{
                  storeData,
                  handleSubmit
                  // Add any other functions or props you want to make available to dynamic components
                }}
              />
              </View>
            </View>
          }

          {
            (!Boolean(uiData) && !isLoading) &&
            <View className="p-6 flex-1 justify-center" key="initial"
              from={{
                opacity: 0,
                scale: 1,
                translateY: 10,
              }}
              animate={{
                opacity: 1,
                scale: 1,
                translateY: 0
              }}
              exit={{
                opacity: 0,
                scale: 0.9,
                translateY: 0
              }}
            >

              <View className="flex gap-2">
                <Text className="text-2xl text-white font-light">Welcome to</Text>
                <Text className="text-4xl text-white font-light"><Text className="font-semibold">Adabtive</Text> Interface</Text>

              </View>

            </View>
          }




          {
            !isLoading &&

            <View key='action-button' className="w-full absolute bottom-0 p-6 items-center justify-center" style={{ marginBottom: insets.bottom }}
              from={{
                opacity: 0,
                //scale: 1,
                translateY: 20,
              }}
              animate={{
                opacity: 1,
                //scale: 1,
                translateY: 0
              }}
              exit={{
                opacity: 0,
                //scale: 0.9,
                translateY: 20
              }}
            >
              <Pressable
                onPress={uiData? reset:fetchDataFromAPI}
                //onPress={() => { setIsLoading(!isLoading) }}
                //disabled={isLoading}
                className="bg-white/20 w-full items-center justify-center p-1 rounded-full flex-row w-80"
              >


                <View className="flex-1 items-center p-4">
                  <Text className="text-white text-lg">{uiData? 'Start Over':'Start'}</Text>
                </View>

              </Pressable>
            </View>
          }

          {
            isLoading &&
            <View className="p-6 flex-1 justify-center" key="loading"
              from={{
                opacity: 0,
                scale: 1.2,
                //translateY: 10,
              }}
              animate={{
                opacity: .8,
                scale: 1,
                //translateY: 0
              }}
              exit={{
                opacity: 0,
                scale: 1.2,
                //translateY: 0
              }}
              transition={{
                type: 'timing',
                duration: 500,  // Duration in milliseconds
                easing: Easing.out(Easing.quad), // Fast to slow transition
              }}
            >
              <VortexSphere />
            </View>
          }

        </AnimatePresence>
      </SafeAreaView>

    </View>
  );
}


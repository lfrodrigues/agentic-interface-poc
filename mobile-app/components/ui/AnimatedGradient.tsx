import {
    TouchableOpacity,
    StyleSheet,
    useWindowDimensions,
  } from 'react-native';
  import { FontAwesome } from '@expo/vector-icons';
  import { Canvas, LinearGradient, Rect, vec } from '@shopify/react-native-skia';
  import {
    useDerivedValue,
    useSharedValue,
    withTiming,
  } from 'react-native-reanimated';
  
  import { getBiasedRandomColor, getRandomColor } from '../../utils';
import { useEffect } from 'react';
  
  const AnimatedGradient = () => {
    const { width, height } = useWindowDimensions();
  
    const leftColor = useSharedValue('#6218be');
    const rightColor = useSharedValue('#c724b1');
    const lastColor = useSharedValue('#94c6d4');
  
    const colors = useDerivedValue(() => {
      return [lastColor.value, rightColor.value,  leftColor.value ];
    }, []);
  
    useEffect(()=>{
        setInterval(()=>{
          lastColor.value = withTiming(getRandomColor(), {duration: 2600});
          rightColor.value = withTiming(getBiasedRandomColor(), {duration: 2600});
            leftColor.value = withTiming(getBiasedRandomColor(), {duration: 3000});
        },3000)
    },[])
    return (
      <>
        <Canvas style={{ flex: 1 , opacity: .4}}>
          <Rect x={0} y={0} width={width} height={height}>
            <LinearGradient
              start={vec(0, 0)}
              end={vec(width, height)}
              colors={colors}
            />
          </Rect>
        </Canvas>
        {/* <TouchableOpacity
          style={styles.buttonContainer}
          onPress={() => {
            
          }}>
          <FontAwesome name="random" size={24} color="white" />
        </TouchableOpacity> */}
      </>
    );
  };
  
  const styles = StyleSheet.create({
    buttonContainer: {
      position: 'absolute',
      bottom: 52,
      right: 32,
      height: 64,
      aspectRatio: 1,
      borderRadius: 40,
      backgroundColor: '#111',
      zIndex: 10,
      justifyContent: 'center',
      alignItems: 'center',
    },
  });
  
  
export default AnimatedGradient;

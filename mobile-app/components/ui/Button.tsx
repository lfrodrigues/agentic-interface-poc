import { View } from 'moti'
import React from 'react'
import { Pressable, PressableProps } from 'react-native'
import Text from './Text'

interface CustomPressableProps extends PressableProps {
    title: string
}

const Button: React.FC<CustomPressableProps> = ({ style, className, title, ...props }) => {
    return (
        <Pressable
            {...props}
            //onPress={() => { setIsLoading(!isLoading) }}
            //disabled={isLoading}
            className="border  border-white/30 w-full items-center justify-center p-1 rounded-full flex-row "
        >
            <View className="flex-1 items-center p-2">
                <Text className="text-white text-xl">{title}</Text>
            </View>

            {/* <View className="bg-white/60 rounded-full p-4">
                  <Feather name="arrow-right" color="#292929" size={20} />
                </View> */}
        </Pressable>
    )
}

export default Button;
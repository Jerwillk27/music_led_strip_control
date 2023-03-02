from libs.effects.effect import Effect  # pylint: disable=E0611, E0401

from scipy.ndimage.filters import gaussian_filter1d
import numpy as np


class EffectHolidayLights(Effect):
    def __init__(self, device):
        
        # Call the constructor of the base class.
        super(EffectHolidayLights, self).__init__(device)
        
        # Setup for "VU Meter" (don't change these)
        self.interval_history = 0
        self.alt = 1
    
    def run(self):
        
        # Get the config of the current effect.
        effect_config = self.get_effect_config("effect_holiday_lights")
        
        self._led_strip = self._device.device_config["led_strip"]
        # Set Fallback Strip
        # self._led_strip_translated = ws.WS2811_STRIP_RGB
        
        # Build an empty array. 
        if "SK6812" in self._led_strip:
            output_array = np.zeros((4, self._device.device_config["led_count"]))
        else:
            output_array = np.zeros((3, self._device.device_config["led_count"]))
            
        if effect_config["use_custom_color"]:
            # Fill the array with the selected color. (0 = red channel, 1 = green channel, 2 = blue channel)
            s = effect_config["led_spacing"]  # This is the number of non-lit LEDs (spacing)
            w = effect_config["led_width"]  # This is the number of lit LEDs (width)
            n = 0  # This will be our counter to keep track of where we're at on the LED string
            e = 1  # enable (write light bits) 1 = yes, 0 = no
            if effect_config["interval_enable"]:
                if self.interval_history >= effect_config["interval"]:
                    if self.alt == 1:
                        self.alt = 2
                    elif self.alt == 2:
                        self.alt = 1   
            else:
                self.alt = 1
                
            for i in range(self._device.device_config["led_count"]):
                if e == 1:
                    # lit LEDs
                    start = n
                    end = n + w
                    if effect_config["alternate"]:
                        if self.alt == 1:
                            output_array[0][start:end] = effect_config["custom_color_1"][0]
                            output_array[1][start:end] = effect_config["custom_color_1"][1]
                            output_array[2][start:end] = effect_config["custom_color_1"][2]
                            self.alt = 2
                        elif self.alt == 2:
                            output_array[0][start:end] = effect_config["custom_color_2"][0]
                            output_array[1][start:end] = effect_config["custom_color_2"][1]
                            output_array[2][start:end] = effect_config["custom_color_2"][2]
                            self.alt = 1
                    else:
                        output_array[0][start:end] = effect_config["custom_color_1"][0]
                        output_array[1][start:end] = effect_config["custom_color_1"][1]
                        output_array[2][start:end] = effect_config["custom_color_1"][2]
                        
                    e = 0
                    n = end
                elif e == 0:
                    # non-lit LEDs
                    start = n
                    end = n + s
                    output_array[0][start:end] = 0
                    output_array[1][start:end] = 0
                    output_array[2][start:end] = 0
                    e = 1
                    n = end
        else:
            # Fill the array with the selected color. (0 = red channel, 1 = green channel, 2 = blue channel)
            s = effect_config["led_spacing"]  # This is the nubmer of non-liet LEDs (spacing)
            w = effect_config["led_width"]  # This is the number of lit LEDs (width)
            n = 0
            e = 1
            if effect_config["interval_enable"]:
                if self.interval_history > = effect_config["interval"]:
                    if self.alt == 1:
                        output_array[0][start:end] = self._config_colours[effect_config["color_1"]][0]
                        output_array[1][start:end] = self._config_colours[effect_config["color_1"]][1]
                        output_array[2][start:end] = self._config_colours[effect_config["color_1"]][2]
                        self.alt = 2
                    elif self.alt == 2:
                        output_array[0][start:end] = self._config_colours[effect_config["color_2"]][0]
                        output_array[1][start:end] = self._config_colours[effect_config["color_2"]][1]
                        output_array[2][start:end] = self._config_colours[effect_config["color_2"]][2]
                        self.alt = 1
                else:
                    output_array[0][start:end] = self._config_colours[effect_config["color_1"]][0]
                    output_array[1][start:end] = self._config_colours[effect_config["color_1"]][1]
                    output_array[2][start:end] = self._config_colours[effect_config["color_1"]][2]
                e = 0
                n = end
            elif e == 0:
                # non-lit LEDs
                start = n
                end = n + s
                output_array[0][start:end] = 0
                output_array[1][start:end] = 0
                output_array[2][start:end] = 0
                e = 0
                n = end
        
        if "SK6812" in self._led_strip:
            output_array[3][:] = effect_config["white"]
            
        # Increment and add the current interval to the interval history
        if self.interval_history >= effect_config["interval"]:
            self.interval_history = 0
        else:
            self.interval_history = self.interval_history + 1
            
        # Persist the current value of alt
        self.alt = self.alt
        
        # Add the output array to the queue.
        self.queue_output_array_blocking(output_array)
          

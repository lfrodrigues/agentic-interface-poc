export const getRandomColor = () => {
    // Generate random RGB color values
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
  
    // Return the color in the format '#RRGGBB'
    return `#${r.toString(16)}${g.toString(16)}${b.toString(16)}`;
  };


  export const getBiasedRandomColor = () => {
    // Base colors (purple and pink-purple)
    const baseColors = [
      { r: 98, g: 24, b: 190 },  // #6218be
      { r: 199, g: 36, b: 177 },  // #c724b1
      // { r: 181, g: 239, b: 255 }, // #b5efff
    ];
  
    // Pick a random base color
    const base = baseColors[Math.floor(Math.random() * baseColors.length)];
  
    // Add slight variation (±30)
    const variation = 30; 
    const r = Math.min(255, Math.max(0, base.r + (Math.random() * variation - variation / 2)));
    const g = Math.min(255, Math.max(0, base.g + (Math.random() * variation - variation / 2)));
    const b = Math.min(255, Math.max(0, base.b + (Math.random() * variation - variation / 2)));
  
    // Convert to HEX format
    return `#${Math.round(r).toString(16).padStart(2, '0')}${Math.round(g).toString(16).padStart(2, '0')}${Math.round(b).toString(16).padStart(2, '0')}`;
  };
  
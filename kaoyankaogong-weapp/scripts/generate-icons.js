const fs = require('fs');
const path = require('path');

const iconDir = path.join(__dirname, '../images');

const crcTable = [];
for (let i = 0; i < 256; i++) {
  let c = i;
  for (let j = 0; j < 8; j++) {
    c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
  }
  crcTable[i] = c;
}

const crc32 = (buf) => {
  let crc = 0xFFFFFFFF;
  for (let i = 0; i < buf.length; i++) {
    crc = crcTable[(crc ^ buf[i]) & 0xFF] ^ (crc >>> 8);
  }
  return crc ^ 0xFFFFFFFF;
};

const createChunk = (type, data) => {
  const chunk = Buffer.alloc(12 + data.length);
  chunk.writeUInt32BE(data.length, 0);
  chunk.write(type, 4, 4, 'ascii');
  data.copy(chunk, 8);
  const crc = crc32(Buffer.concat([Buffer.from(type), data]));
  chunk.writeUInt32BE(crc >>> 0, 8 + data.length);
  return chunk;
};

const createPNG = (width, height, draw) => {
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0);
  ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8;
  ihdr[9] = 6;
  ihdr[10] = 0;
  ihdr[11] = 0;
  ihdr[12] = 0;

  const rawData = Buffer.alloc((width * 4 + 1) * height);
  for (let y = 0; y < height; y++) {
    rawData[y * (width * 4 + 1)] = 0;
    for (let x = 0; x < width; x++) {
      const idx = y * (width * 4 + 1) + 1 + x * 4;
      const [r, g, b, a] = draw(x, y, width, height);
      rawData[idx] = r;
      rawData[idx + 1] = g;
      rawData[idx + 2] = b;
      rawData[idx + 3] = a;
    }
  }

  const zlib = require('zlib');
  const compressed = zlib.deflateSync(rawData);

  const ihdrChunk = createChunk('IHDR', ihdr);
  const idatChunk = createChunk('IDAT', compressed);
  const iendChunk = createChunk('IEND', Buffer.alloc(0));

  const totalSize = 8 + ihdrChunk.length + idatChunk.length + iendChunk.length;
  const png = Buffer.alloc(totalSize);
  
  png.writeUInt32BE(0x89504E47, 0);
  png.writeUInt32BE(0x0D0A1A0A, 4);
  
  let offset = 8;
  ihdrChunk.copy(png, offset);
  offset += ihdrChunk.length;
  idatChunk.copy(png, offset);
  offset += idatChunk.length;
  iendChunk.copy(png, offset);

  return png;
};

const homeIcon = (color) => {
  return (x, y, w, h) => {
    const cx = w / 2, cy = h / 2;
    const r = Math.min(w, h) * 0.35;
    
    if (y >= cy - r && y <= cy + r * 0.5) {
      if (x >= cx - r * 0.8 && x <= cx + r * 0.8) {
        return color;
      }
    }
    
    if (y >= cy + r * 0.5 && y <= cy + r) {
      if (x >= cx - r && x <= cx + r) {
        return color;
      }
    }
    
    if (y >= cy - r * 1.2 && y <= cy - r * 0.3) {
      const dx = Math.abs(x - cx);
      const dy = cy - r * 0.3 - y;
      if (dx <= dy * 0.6) {
        return color;
      }
    }
    
    return [0, 0, 0, 0];
  };
};

const infoIcon = (color) => {
  return (x, y, w, h) => {
    const cx = w / 2, cy = h / 2;
    const r = Math.min(w, h) * 0.3;
    
    if (Math.sqrt((x - cx) ** 2 + (y - cy) ** 2) <= r) {
      return color;
    }
    
    if (y >= cy - r * 0.1 && y <= cy + r * 0.1) {
      if (x >= cx - r * 0.7 && x <= cx - r * 0.2) {
        return color;
      }
    }
    
    if (y >= cy + r * 0.2 && y <= cy + r * 0.7) {
      if (x >= cx - r * 0.7 && x <= cx - r * 0.2) {
        return color;
      }
    }
    
    return [0, 0, 0, 0];
  };
};

const messageIcon = (color) => {
  return (x, y, w, h) => {
    const cx = w / 2, cy = h / 2;
    const r = Math.min(w, h) * 0.35;
    
    if (Math.sqrt((x - cx) ** 2 + (y - cy) ** 2) <= r) {
      return color;
    }
    
    const tailX = cx + r * 1.2;
    const tailY = cy + r * 0.6;
    
    if (x >= cx + r * 0.5 && x <= tailX) {
      const slope = (tailY - cy) / (tailX - cx);
      const dist = Math.abs(slope * (x - cx) - (y - cy)) / Math.sqrt(slope ** 2 + 1);
      if (dist <= 6) {
        return color;
      }
    }
    
    return [0, 0, 0, 0];
  };
};

const userIcon = (color) => {
  return (x, y, w, h) => {
    const cx = w / 2, cy = h / 2;
    const headR = Math.min(w, h) * 0.2;
    const bodyW = Math.min(w, h) * 0.35;
    const bodyH = Math.min(w, h) * 0.4;
    
    if (Math.sqrt((x - cx) ** 2 + (y - cy + bodyH * 0.2) ** 2) <= headR) {
      return color;
    }
    
    if (x >= cx - bodyW / 2 && x <= cx + bodyW / 2) {
      if (y >= cy - bodyH * 0.1 && y <= cy + bodyH * 0.9) {
        return color;
      }
    }
    
    return [0, 0, 0, 0];
  };
};

const icons = {
  'home': homeIcon,
  'info': infoIcon,
  'message': messageIcon,
  'user': userIcon
};

const normalColor = [102, 102, 102, 255];
const activeColor = [24, 144, 255, 255];

if (!fs.existsSync(iconDir)) {
  fs.mkdirSync(iconDir, { recursive: true });
}

Object.entries(icons).forEach(([name, drawFn]) => {
  const normalPng = createPNG(48, 48, drawFn(normalColor));
  const activePng = createPNG(48, 48, drawFn(activeColor));
  
  fs.writeFileSync(path.join(iconDir, `${name}.png`), normalPng);
  fs.writeFileSync(path.join(iconDir, `${name}-active.png`), activePng);
  
  console.log(`Created ${name}.png and ${name}-active.png`);
});

console.log('All icons generated successfully!');
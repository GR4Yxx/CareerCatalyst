// This script converts the Career Catalyst icon SVG to an ICO file
const fs = require('fs')
const path = require('path')
const sharp = require('sharp')

// Create a Career Catalyst themed favicon
// Since we can't install Sharp directly, this is a script that would work
// if Sharp was installed. For now, we'll create a placeholder with instructions.

console.log('To generate a favicon:')
console.log('1. Install Sharp: npm install sharp --save-dev')
console.log('2. Run this script: node build-tools/create-favicon.js')
console.log('3. The favicon.ico will be placed in the public directory')

// This would be the implementation if Sharp was installed:
/*
async function createFavicon() {
  const svgPath = path.join(__dirname, '../src/assets/svgs/icon-dark.svg');
  const svgBuffer = fs.readFileSync(svgPath);

  // Create different sizes for the favicon
  const sizes = [16, 32, 48, 64];
  const images = await Promise.all(
    sizes.map(size =>
      sharp(svgBuffer)
        .resize(size, size)
        .toBuffer()
    )
  );

  // Write to favicon.ico
  const faviconPath = path.join(__dirname, '../public/favicon.ico');
  fs.writeFileSync(faviconPath, Buffer.concat(images));

  console.log(`Favicon created at ${faviconPath}`);
}

createFavicon().catch(console.error);
*/

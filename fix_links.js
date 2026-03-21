const fs = require('fs');
const path = require('path');

const linksDir = path.join(__dirname, 'links');
const templatePath = path.join(linksDir, 'template.html');
let templateHtml = '';

try {
    templateHtml = fs.readFileSync(templatePath, 'utf8');
} catch (e) {
    console.error('Template not found');
    process.exit(1);
}

function slugify(text) {
    return text.toLowerCase()
        .replace(/ /g, '-')
        .replace(/\//g, '')
        .replace(/[()]/g, '')
        .replace(/&/g, '')
        .replace(/–/g, '-') // en dash
        .replace(/—/g, '-') // em dash
        .replace(/--+/g, '-')
        .replace(/^-+|-+$/g, '');
}

// Keep reading until no more new files are found? 
// No, the new files created will also have the same templates, which don't have hardcoded external URLs in the Related/Latest posts block.
// Wait, actually template.html DOES NOT have the Latest/Related Posts block at the bottom! So new files won't have external links to replace.

const files = fs.readdirSync(linksDir).filter(f => f.endsWith('.html') && f !== 'template.html');

let updatedFiles = 0;
let newFilesCreated = 0;

files.forEach(file => {
    const filePath = path.join(linksDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    let changed = false;

    // Fix external sarkari links
    const regex = /<a\s+[^>]*href=["'](https?:\/\/(?:www\.)?sarkariresult\.com\.cm\/[^"']*)["'][^>]*>(.*?)<\/a>/gi;

    content = content.replace(regex, (match, url, linkText) => {
        let cleanText = linkText.replace(/<[^>]*>/g, ' ')
                                .replace(/&[^;]+;/g, ' ')
                                .replace(/[^a-zA-Z0-9 -]/g, ' ')
                                .trim();
        if (!cleanText) return match; 
        
        const slug = slugify(cleanText);
        const newHref = `${slug}.html`; 
        
        const targetPath = path.join(linksDir, newHref);
        if (!fs.existsSync(targetPath)) {
            // Create the missing rollout page
            const newPageContent = templateHtml.replace(/\{\{TITLE\}\}/g, cleanText);
            fs.writeFileSync(targetPath, newPageContent, 'utf8');
            newFilesCreated++;
        }

        changed = true;
        // Return relative href to same directory
        return `<a href="${newHref}">${linkText}</a>`;
    });

    if (changed) {
        fs.writeFileSync(filePath, content, 'utf8');
        updatedFiles++;
    }
});

console.log(`Finished fixing links! Updated ${updatedFiles} existing files. Created ${newFilesCreated} new rollout pages.`);

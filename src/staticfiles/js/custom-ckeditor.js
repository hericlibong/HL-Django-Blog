
document.addEventListener('DOMContentLoaded', function() {
    // Sélectionnez tous les éléments pre générés par le plugin CodeSnippet
    var codeBlocks = document.querySelectorAll('pre.cke_codeSnippetContainer');

    // Appliquez des styles personnalisés à ces éléments
    codeBlocks.forEach(function(codeBlock) {
        codeBlock.style.fontFamily = 'Courier New, monospace';
        codeBlock.style.fontSize = '14px';
        codeBlock.style.backgroundColor = '#f7f7f7';
        codeBlock.style.padding = '10px';
        codeBlock.style.border = '1px solid #ddd';
        codeBlock.style.borderRadius = '4px';
        codeBlock.style.maxWidth = '50%'; // Ajustez la largeur maximale selon vos besoins
        codeBlock.style.margin = '0 auto';
    });
});

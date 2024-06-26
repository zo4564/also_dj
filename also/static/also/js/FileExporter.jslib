mergeInto(LibraryManager.library, {
    DownloadFile: function (filename, jsonData) {
        var a = document.createElement('a');
        var file = new Blob([Pointer_stringify(jsonData)], { type: 'application/json' });
        a.href = URL.createObjectURL(file);
        a.download = Pointer_stringify(filename);
        a.click();
    }
}); 

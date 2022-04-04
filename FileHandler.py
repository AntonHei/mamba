import os
import magic
import subprocess

class FileHandler():

    file_extension_mimeType = {
        'html': 'text/html',
        'php': 'application/php',
        'css': 'text/css',
    }

    file_extension_mimeTypeHeader = {
        'php': 'text/html',
    }

    rootDirectory = "C:\\mamba-server"
    phpPath = "C:\\php\\php-cgi.exe"

    def getFilePath(self, file_name):
        filePath = self.rootDirectory + "\\" + file_name
        return filePath

    def getFileExtensionByFileName(self, file_name):
        extension = None

        if '.' in file_name:
            parts = file_name.rsplit('.', 1)
            extension = parts[-1]

        return extension

    def getFileMimeTypeByFileName(self, file_name):
        mimeType = "text/plain"
        extension = self.getFileExtensionByFileName(file_name)
        if extension:
            if extension in self.file_extension_mimeType:
                if self.file_extension_mimeType[extension]:
                    mimeType = self.file_extension_mimeType[extension]

        return mimeType

    def getFileMimeType(self, file_name):
        mimeType = None
        filePath = self.getFilePath(file_name)
        if self.doesFileExist(file_name):
            mimeType = self.getFileMimeTypeByFileName(file_name)

            if mimeType == "text/plain":
                mime = magic.Magic(mime=True)
                mimeType = mime.from_file(filePath)

        return mimeType

    def getFileMimeTypeForHeader(self, file_name):
        mimeType = self.getFileMimeType(file_name)
        extension = self.getFileExtensionByFileName(file_name)
        if extension in self.file_extension_mimeTypeHeader:
            headerMimeType = self.file_extension_mimeTypeHeader[extension]
            if headerMimeType:
                return headerMimeType

        return mimeType

    def executePHP(self, file_name):
        out = None

        filePath = self.getFilePath(file_name)
        mimeType = self.getFileMimeType(file_name)
        if mimeType == "application/php":
            process = subprocess.run(f"\"{self.phpPath}\" \"{filePath}\"", stdout=subprocess.PIPE, shell=True)
            out = process.stdout

        return out

    def doesFileExist(self, file_name):
        filePath = self.getFilePath(file_name)
        exists = os.path.exists(filePath)
        return exists

    def isFolder(self, file_name):
        filePath = self.getFilePath(file_name)
        isFolder = os.path.isdir(filePath)
        return isFolder

    def canAccessFile(self, file_name):
        filePath = self.getFilePath(file_name)
        canAccess = os.access(filePath, os.R_OK)
        return canAccess

    def loadRequestedFile(self, file_name):
        fileContent = None
        if self.doesFileExist(file_name):
            filePath = self.getFilePath(file_name)
            try:
                fileStream = open(filePath, "rb")
                fileContent = fileStream.read()
                fileStream.close()
            except PermissionError:
                return None

        return fileContent

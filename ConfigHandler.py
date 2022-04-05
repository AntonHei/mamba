import os
import json
from glob import glob

class ConfigHandler():

    config_extension = "json"

    # Runtime Variables
    loadedConfigs = {}

    def __init__(self):
        self.loadConfigs()

    def getConfigData(self, configIndex):
        configData = None

        if configIndex in self.loadedConfigs:
            configData = self.loadedConfigs[configIndex]

        return configData

    def loadConfigs(self):
        configFiles = self.getConfigFilenames()
        for configPath in configFiles:
            fullFilename = os.path.basename(configPath)
            configIndex = os.path.splitext(fullFilename)[0]
            configContent = self.loadConfig(configPath)
            configContentJSON = json.loads(configContent)
            self.loadedConfigs[configIndex] = configContentJSON

    def getConfigFilenames(self):
        files = glob(f"configs/*.{self.config_extension}")
        return files

    def doesFileExist(self, filePath):
        exists = os.path.exists(filePath)
        return exists

    def loadConfig(self, configFilePath):
        fileContent = None
        if self.doesFileExist(configFilePath):
            try:
                fileStream = open(configFilePath, "r")
                fileContent = fileStream.read()
                fileStream.close()
            except Exception:
                return fileContent

        return fileContent
import os
import csv
import shutil
import time
from typing import Iterator, Dict

class DatasetCreator:
    @staticmethod
    def is_dir_executable(dir_path: str) -> bool:
        """
        Validate whether given path is a directory and if user has access.
        """
        if not(os.path.isdir(dir_path) and os.access(dir_path, os.X_OK)):
            return False
        return True
    

    def __init__(self, input_dir_path: str, output_dir_path: str, class_dict: Dict[str, int]):

        if self.is_dir_executable(input_dir_path) and self.is_dir_executable(output_dir_path):
            self.input_dir_path = input_dir_path 
            self.output_dir_path = output_dir_path
            self.init_output_csv()
            self.class_dict = class_dict
            self.input_image_iter = os.scandir(input_dir_path)
        else:
            raise PermissionError("Input/Output Directory/Permissions Not Set.")
        

    def iter_images_in_dir(self) -> Iterator[os.DirEntry]:
        """
        Returns an iterator over the file names that have given extension(s).
        """
        
        try:
            filename = next(self.input_image_iter)
            if os.path.splitext(filename.name)[-1] in ['.jpg', '.png']:
                return filename.path
        except StopIteration:
            raise FileNotFoundError


    def convert_label_to_int(self, label: str) -> int:
        """
        Convert selected label to int. 
        """
        return self.class_dict[label]
    

    def init_output_csv(self): 
        """
        Create initial header row of output csv.
        """
        with open (os.path.join(self.output_dir_path, "classes.csv"), "w") as file:
            writer = csv.writer(file)
            writer.writerow(["filepath", "class"])


    def label_and_save(self, file_path: str, selected_label: str): 
        """
        Labels and saves images. 
        """

        label_int = self.convert_label_to_int(selected_label)
        output_filename = str(time.time()).replace(".", "") + os.path.splitext(file_path)[1]
        output_filepath = os.path.join(self.output_dir_path, output_filename)
        shutil.copyfile(file_path, output_filepath)
        # shutil.move(file_path, output_filepath)
        
        with open (os.path.join(self.output_dir_path, "classes.csv"), "a") as file:
            writer = csv.writer(file)
            writer.writerow([output_filepath, label_int])
        
        return None, None
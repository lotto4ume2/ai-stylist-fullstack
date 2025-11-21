"use client";

import { useState, useCallback } from 'react';

interface DragDropUploadProps {
  onFileSelect: (file: File) => void;
  accept?: string;
  maxSize?: number; // in MB
}

export default function DragDropUpload({ 
  onFileSelect, 
  accept = "image/*",
  maxSize = 10 
}: DragDropUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState('');

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDragIn = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      setIsDragging(true);
    }
  }, []);

  const handleDragOut = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const validateFile = (file: File): string | null => {
    // Check file type
    if (!file.type.startsWith('image/')) {
      return 'Please upload an image file';
    }

    // Check file size
    const sizeMB = file.size / (1024 * 1024);
    if (sizeMB > maxSize) {
      return `File size must be less than ${maxSize}MB`;
    }

    return null;
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    setError('');

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      const file = files[0];
      const validationError = validateFile(file);
      
      if (validationError) {
        setError(validationError);
        return;
      }

      onFileSelect(file);
    }
  }, [onFileSelect, maxSize]);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError('');
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      const validationError = validateFile(file);
      
      if (validationError) {
        setError(validationError);
        return;
      }

      onFileSelect(file);
    }
  };

  return (
    <div className="w-full">
      <div
        onDragEnter={handleDragIn}
        onDragLeave={handleDragOut}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-lg p-8 text-center
          transition-all duration-300 ease-in-out
          ${isDragging 
            ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 scale-105' 
            : 'border-gray-300 dark:border-gray-600 hover:border-purple-400 dark:hover:border-purple-500'
          }
          ${error ? 'border-red-500' : ''}
        `}
      >
        <input
          type="file"
          accept={accept}
          onChange={handleFileInput}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          id="file-upload"
        />
        
        <div className="pointer-events-none">
          <div className="mb-4">
            <svg
              className={`mx-auto h-12 w-12 transition-transform duration-300 ${
                isDragging ? 'scale-110 text-purple-500' : 'text-gray-400 dark:text-gray-500'
              }`}
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
              aria-hidden="true"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          
          <div className="text-sm text-gray-600 dark:text-gray-400">
            <label
              htmlFor="file-upload"
              className="relative cursor-pointer rounded-md font-medium text-purple-600 dark:text-purple-400 hover:text-purple-500 focus-within:outline-none"
            >
              <span>Upload a file</span>
            </label>
            <p className="pl-1">or drag and drop</p>
          </div>
          
          <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
            PNG, JPG, WEBP up to {maxSize}MB
          </p>
        </div>
      </div>

      {error && (
        <div className="mt-2 text-sm text-red-600 dark:text-red-400 animate-fade-in">
          {error}
        </div>
      )}
    </div>
  );
}

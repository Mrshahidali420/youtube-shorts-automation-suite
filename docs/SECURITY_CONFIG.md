# Secure Configuration Guide

This guide explains how to securely configure the YouTube Shorts Automation Suite to protect sensitive information like API keys.

## Security Best Practices

### API Keys Protection

1. **Never commit API keys to public repositories**
   - Keep your `config.txt` file out of version control
   - The `.gitignore` file is already set up to exclude `config.txt`

2. **Use environment variables for sensitive information**
   - Set environment variables with the prefix `YT_SHORTS_`
   - Example: `YT_SHORTS_API_KEY=your_api_key_here`

3. **Regularly rotate your API keys**
   - Periodically generate new API keys, especially for production environments
   - Update your configuration with the new keys

4. **Set appropriate API key restrictions**
   - In Google Cloud Console, restrict your API keys to only the necessary APIs
   - Consider adding IP restrictions if your automation runs from a fixed location

## Configuration Methods

### Method 1: Using config.txt (Recommended for Development)

1. Copy the template to create your configuration file:
   ```
   cp templates/config.txt.template config.txt
   ```

2. Edit `config.txt` and add your API keys and other settings:
   ```
   API_KEY=your_gemini_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. Ensure `config.txt` is in your `.gitignore` file to prevent accidental commits

### Method 2: Using Environment Variables (Recommended for Production)

1. Set environment variables with the `YT_SHORTS_` prefix:

   **Windows:**
   ```
   set YT_SHORTS_API_KEY=your_gemini_api_key_here
   set YT_SHORTS_GEMINI_API_KEY=your_gemini_api_key_here
   ```

   **Linux/macOS:**
   ```
   export YT_SHORTS_API_KEY=your_gemini_api_key_here
   export YT_SHORTS_GEMINI_API_KEY=your_gemini_api_key_here
   ```

2. Environment variables will override settings in `config.txt`

### Method 3: Using a Secure Secrets Manager (Advanced)

For production environments, consider using a secure secrets manager:

1. **Windows:** Use Windows Credential Manager
2. **Linux:** Use tools like HashiCorp Vault or AWS Secrets Manager
3. **Cloud:** Use cloud-specific secrets management services

## Verifying Your Configuration

Run the secure configuration test to verify your setup:

```
python secure_config.py
```

This will:
1. Create an example configuration file if it doesn't exist
2. Test loading your configuration
3. Display your configuration with sensitive values masked

## Troubleshooting

If you encounter configuration issues:

1. Check that your `config.txt` file exists and has the correct format
2. Verify that environment variables are set correctly
3. Ensure you have the necessary permissions to read the configuration file
4. Check the logs for specific error messages

## Additional Security Measures

1. **File Permissions:**
   - Restrict permissions on your `config.txt` file
   - On Linux/macOS: `chmod 600 config.txt`
   - On Windows: Set appropriate NTFS permissions

2. **Secure Storage:**
   - Consider encrypting sensitive configuration files
   - Use secure storage solutions for production environments

3. **Audit Trail:**
   - Keep track of who has access to API keys
   - Implement logging for configuration access

Remember that security is a continuous process. Regularly review and update your security practices to protect your sensitive information.

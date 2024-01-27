function rsa_gui()
Modulu_s = ''
PrivateExponent_s=''
cipher_s= ''
    % Create the main GUI window
    fig = figure('Name', 'RSA Encryption and Decryption', 'NumberTitle', 'off', 'Position', [300, 300, 600, 400]);

    % Constant Values
    publicKey = '';
    privateKey = '';

    % Text or File Input
    uicontrol(fig, 'Style', 'text', 'Position', [10 350 100 20], 'String', 'Text:');
    textInput = uicontrol(fig, 'Style', 'edit', 'Position', [120 350 270 20]);

    % Record Button
   

    % Operation Selection
    uicontrol(fig, 'Style', 'text', 'Position', [10 320 100 20], 'String', 'Operation:');
    operationInput = uicontrol(fig, 'Style', 'popupmenu', 'Position', [120 320 270 20], 'String', {'Encrypt', 'Decrypt'});

    % Execute Button
    executeButton = uicontrol(fig, 'Style', 'pushbutton', 'Position', [150 290 100 30], 'String', 'Execute', 'Callback', @executeOperation);
    
     recordButton = uicontrol(fig, 'Style', 'pushbutton', 'Position', [420 290 100 30], 'String', 'Record', 'Callback', @recordAudio);
    
    % Output Display
    resultOutput = uicontrol(fig, 'Style', 'edit', 'Position', [10 50 380 230], 'Max', 2, 'Min', 0, 'Enable', 'inactive');

    % Play Buttons
    uicontrol(fig, 'Style', 'pushbutton', 'Position', [420 290 100 30], 'String', 'Play Original', 'Callback', @playOriginal);
    uicontrol(fig, 'Style', 'pushbutton', 'Position', [420 250 100 30], 'String', 'Play Encrypted', 'Callback', @playEncrypted);
    uicontrol(fig, 'Style', 'pushbutton', 'Position', [420 210 100 30], 'String', 'Play Decrypted', 'Callback', @playDecrypted);
    
     fs = 8000; % Sampling frequency

    % Initialize recorder and player
    recObj = audiorecorder(fs, 8, 1);

    % Callback Function for Execute Button
    function executeOperation(~, ~)
        text = get(textInput, 'String');
        operation = get(operationInput, 'Value');

        try
               if operation == 1 % Encrypt
                [cipher, privateKey,moduls] = encryptRSA(text);
                cipher_s =cipher
                PrivateExponent_s=privateKey
                Modulu_s = moduls
                set(resultOutput, 'String', ['Cipher: ', cipher, char(10), 'Public Key: ', moduls, char(10), 'Private Key: ', privateKey]);
            elseif operation == 2 % Decrypt
                cipher = get(resultOutput, 'String');
                plain = decryptRSA(cipher_s, PrivateExponent_s,Modulu_s);
                set(resultOutput, 'String', ['Decrypted Text: ', plain]);
            end
        catch e
            set(resultOutput, 'String', ['Error: ', e.message]);
        end
    end


      function recordAudio(~, ~)
        disp('Recording started. Speak into the microphone...');
        record(recObj);
        pause(5); % Record for 5 seconds
        stop(recObj);
        disp('Recording stopped.');
        y = getaudiodata(recObj, 'uint8');
        xlswrite('RSA_original_voice.xlsx', int32(y));
    end

    % Callback Function for "Play Original" Button
    function playOriginal(~, ~)
        fs = 8000;
        rec = audiorecorder(fs, 8, 1);
        recordblocking(rec, 5);
        original = getaudiodata(rec);
        sound(original, fs);
    end

    % Callback Function for "Play Encrypted" Button
    function playEncrypted(~, ~)
        % Assumes that 'RSA_encrypted_voice.xlsx' contains the encrypted voice
        en = uigetfile('*.xlsx', 'Select RSA_encrypted_voice.xlsx');
        encrypted = xlsread(en);
        sound(encrypted, fs);
    end

    % Callback Function for "Play Decrypted" Button
    function playDecrypted(~, ~)
        % Assumes that 'RSA_decrypted_voice.xlsx' contains the decrypted voice
        dec = xlsread('RSA_decrypted_voice.xlsx');
        sound(dec, fs);
    end
end


function  [cipher,PrivateExponent,Modulus] = encryptRSA(data)
    
    
    
    [Modulus, PublicExponent, PrivateExponent] = GenerateKeyPair
    pvKey = PrivateExponent
    Message = int32(data)
    modulskey = Modulus
    cipher=Encrypt(Modulus, PublicExponent, Message)
    end

function [plain] = decryptRSA(cipherText, PrivateExponent, Modulus)
    decipher1 = Decrypt(Modulus, PrivateExponent, cipherText);
    plain = char(decipher1);
end

function [cipher, PrivateExponent, Modulus] = encryptVoiceRSA(Modulus, PrivateExponent)
    clc
    clear
    close all
    [Modulus, PublicExponent, PrivateExponent] = GenerateKeyPair;
    pvKey = PrivateExponent;

    fs = 8000;

    % Recording
    rec = audiorecorder(fs, 8, 1);
    msg1 = msgbox('Recording for 5 seconds');
    recordblocking(rec, 5);
    delete(msg1);
    msg2 = msgbox('Recording done');

    % Get data from recorded voice
    y = getaudiodata(rec, 'uint8');
    original = int32(y);
    
    % Plot original voice
    figure(1);
    plot(y);
    title('Original Voice');

    % Write original voice data to xlsx
    xlswrite('RSA_original_voice.xlsx', original);

    % Play original voice
    sound(y, fs);

    % Encrypting voice using public key (e, n)
    cipher = Encrypt(Modulus, PublicExponent, original);

    % Plot encrypted voice
    figure(2);
    plot(cipher);
    title('Encrypted Voice');

    % Write encrypted voice data to xlsx
    xlswrite('RSA_encrypted_voice.xlsx', cipher);
    sound(cipher, fs);
end

function [cipher, PrivateExponent, Modulus] = decryptVoiceRSA(Modulus, PrivateExponent, cipherText)
    % Common sampling frequency for voice
    fs = 8000;

    % Upload encrypted voice data
    % Select 'RSA_encrypted_voice.xlsx'
    en = uigetfile('*.xlsx', 'Select RSA_encrypted_voice.xlsx');
    encrypted = xlsread(en);

    % Plot encrypted voice
    figure(1);
    plot(encrypted);
    title('Encrypted Voice');

    % Play encrypted voice
    sound(encrypted, fs);

    % Decrypting
    decrypted = Decrypt(Modulus, PrivateExponent, cipherText);

    % Plot decrypted voice
    figure(2);
    plot(decrypted);
    title('Decrypted Voice');

    % Write decrypted voice data to xlsx
    xlswrite('RSA_decrypted_voice.xlsx', decrypted);

    % Play decrypted voice
    sound(decrypted, fs);
end

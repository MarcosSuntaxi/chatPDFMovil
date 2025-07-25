import axios from 'axios';
import * as DocumentPicker from 'expo-document-picker';
import * as FileSystem from 'expo-file-system';
import React, { useState } from 'react';
import { ActivityIndicator, Alert, Button, Text, TextInput, View } from 'react-native';

const BACKEND_URL = 'http://192.168.232.138:5000'; // Cambia por tu IP local

export default function Explore() {
  const [pdfName, setPdfName] = useState('');
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [tokensUsed, setTokensUsed] = useState<number | null>(null);
  const [status, setStatus] = useState('');

  const handlePickPdf = async () => {
    setLoading(true);
    setStatus('');
    setPdfName('');
    setAnswer('');
    setTokensUsed(null); // Limpio tokens al subir nuevo pdf
    try {
      const result = await DocumentPicker.getDocumentAsync({ type: 'application/pdf' });
      console.log('DocumentPicker result:', result);

      if (!result.canceled && result.assets && result.assets.length > 0) {
        const asset = result.assets[0];
        setPdfName(asset.name);
        setStatus('Procesando archivo...');

        const fileUri = asset.uri;
        const fileBase64 = await FileSystem.readAsStringAsync(fileUri, { encoding: FileSystem.EncodingType.Base64 });

        setStatus('Subiendo archivo...');
        const res = await axios.post(
          `${BACKEND_URL}/upload`,
          {
            file: fileBase64,
            filename: asset.name,
          },
          {
            headers: { 'Content-Type': 'application/json' }
          }
        );

        setStatus(res.data.message || 'Archivo subido correctamente');
        Alert.alert('PDF', res.data.message || 'Archivo subido correctamente');
      } else if (result.canceled) {
        setStatus('Selección cancelada por el usuario.');
      } else {
        setStatus('No se seleccionó ningún archivo.');
        Alert.alert('Error', 'No se seleccionó ningún archivo.');
      }
    } catch (err: any) {
      setStatus('Error al subir el PDF');
      Alert.alert('Error', err.response?.data?.message || err.message || 'No se pudo subir el PDF');
    }
    setLoading(false);
  };

  const handleAsk = async () => {
    setLoading(true);
    setAnswer('');
    setTokensUsed(null); // Limpio tokens cuando hago nueva pregunta
    setStatus('');
    try {
      const res = await axios.post(
        `${BACKEND_URL}/ask`,
        { question: question },
        { headers: { 'Content-Type': 'application/json' } }
      );
      setAnswer(res.data.answer);
      setTokensUsed(res.data.tokens_used ?? null);
      setStatus('Respuesta recibida');
    } catch (err: any) {
      setStatus('Error al obtener respuesta');
      Alert.alert('Error', err.response?.data?.message || err.message || 'No se pudo obtener respuesta');
    }
    setLoading(false);
  };

  return (
    <View style={{ flex: 1, padding: 16, backgroundColor: '#f7f7f7' }}>
      <View style={{ marginTop: 60 }}>
        <Button title="Seleccionar PDF" onPress={handlePickPdf} disabled={loading} color="#2196F3" />
      </View>
      {pdfName ? <Text style={{ marginTop: 10, fontWeight: 'bold', color: '#2196F3' }}>PDF seleccionado: {pdfName}</Text> : null}
      {status ? <Text style={{ marginTop: 10, color: '#555' }}>{status}</Text> : null}

      <TextInput
        style={{ borderWidth: 1, marginVertical: 16, padding: 8, backgroundColor: '#fff', borderRadius: 6 }}
        placeholder="Escribe tu pregunta"
        value={question}
        onChangeText={setQuestion}
        editable={!loading}
      />
      <Button
        title="Preguntar"
        onPress={handleAsk}
        disabled={loading || !question.trim()}
        color="#90CAF9"
      />

      {loading && (
        <ActivityIndicator size="large" style={{ marginTop: 16 }} color="#2196F3" />
      )}

      {answer ? (
        <View style={{ marginTop: 16, backgroundColor: '#e3f2fd', padding: 12, borderRadius: 6 }}>
          <Text style={{ fontWeight: 'bold', color: '#1565c0' }}>Respuesta:</Text>
          <Text style={{ color: '#1565c0' }}>{answer}</Text>
          {tokensUsed !== null && (
            <Text style={{ marginTop: 8, fontStyle: 'italic', color: '#555' }}>
              Tokens usados: {tokensUsed}
            </Text>
          )}
        </View>
      ) : null}
    </View>
  );
}

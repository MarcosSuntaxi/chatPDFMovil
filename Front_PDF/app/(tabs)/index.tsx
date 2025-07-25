import React from 'react';
import {
  Image,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Linking,
} from 'react-native';
import { Video } from 'expo-av';

export default function HomeScreen() {
  const handlePressThreads = () => {
    Linking.openURL('https://www.threads.net/@marcos.alexander.31');
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Avatar con video */}
      <View style={styles.avatarContainer}>
        <View style={styles.avatarCircle}>
          <Video
            source={require('../../assets/videos/videoExam.mp4')}
            style={styles.avatarVideo}
            resizeMode="cover"
            shouldPlay
            isLooping
            isMuted
          />
        </View>

        {/* Enlace a Threads */}
        <TouchableOpacity onPress={handlePressThreads}>
          <Text style={styles.threadsText}>@marcos.alexander.31 (Threads)</Text>
        </TouchableOpacity>
      </View>

      {/* Nombre y email */}
      <Text style={styles.name}>Marcos Suntaxi</Text>
      <Text style={styles.email}>masuntaxic@uce.edu.ec</Text>

      {/* Quién soy */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>¿Quién soy?</Text>
        <Text style={styles.sectionText}>Soy un estudiante de Sistemas de Información en la Universidad Central del Ecuador apasionado por la tecnología, el desarrollo de software y la innovación. Me destaco por ser proactivo, curioso y comprometido con mis proyectos académicos y personales.</Text>
      </View>

      {/* Virtudes y conocimientos */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Virtudes y Conocimientos</Text>
        <View style={styles.bulletItem}>
          <Text style={styles.bullet}>🟢</Text>
          <Text style={styles.bulletText}>Dominio de programación web y móvil (React, React Native)</Text>
        </View>
        <View style={styles.bulletItem}>
          <Text style={styles.bullet}>🟢</Text>
          <Text style={styles.bulletText}>Experiencia en pruebas de rendimiento con JMeter</Text>
        </View>
        <View style={styles.bulletItem}>
          <Text style={styles.bullet}>🟢</Text>
          <Text style={styles.bulletText}>Conocimientos sólidos en normativas NIST 800</Text>
        </View>
        <View style={styles.bulletItem}>
          <Text style={styles.bullet}>🟢</Text>
          <Text style={styles.bulletText}>Capacidad para integraciones con IA (LangChain, OpenAI)</Text>
        </View>
        <View style={styles.bulletItem}>
          <Text style={styles.bullet}>🟢</Text>
          <Text style={styles.bulletText}>Responsable, autodidacta y con habilidades para el trabajo en equipo</Text>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
  },
  avatarContainer: {
    marginTop: 40,
    marginBottom: 16,
    alignItems: 'center',
  },
  avatarCircle: {
    backgroundColor: '#f2f2f2',
    width: 120,
    height: 120,
    borderRadius: 60,
    overflow: 'hidden',
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarVideo: {
    width: '100%',
    height: '100%',
  },
  threadsText: {
    fontSize: 16,
    color: '#0077b6',
    textDecorationLine: 'underline',
    marginTop: 8,
  },
  name: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#222',
    textAlign: 'center',
    marginTop: 8,
  },
  email: {
    fontSize: 16,
    color: '#888',
    textAlign: 'center',
    marginBottom: 24,
  },
  bottomSection: {
    flex: 1,
    width: '100%',
    backgroundColor: 'rgb(232, 225, 242)',
    alignItems: 'center',
    justifyContent: 'center',
    borderTopLeftRadius: 40,
    borderTopRightRadius: 40,
    paddingTop: 40,
  },
  editButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 18,
  },
  descriptionBox: {
    backgroundColor: '#fff',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: 'rgb(145, 89, 224)',
    paddingVertical: 16,
    paddingHorizontal: 32,
    marginBottom: 24,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 2,
  },
  descriptionText: {
    color: '#222',
    fontSize: 16,
    textAlign: 'center',
  },
});

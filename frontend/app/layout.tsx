import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'MeetBot',
  description: 'AI-Powered Meeting Assistant',
  icons: {
    icon: '/logo.png',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}

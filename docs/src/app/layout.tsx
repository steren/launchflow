import { type Metadata } from 'next'
import { Inter } from 'next/font/google'
import localFont from 'next/font/local'
import clsx from 'clsx'
import { Suspense } from "react";
import { Providers, PHProvider, PostHogPageview } from '@/app/providers'
import { Layout } from '@/components/Layout'

import '@/styles/globals.css'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

// useTheme("dark")

// Use local version of Lexend so that we can use OpenType features
const lexend = localFont({
  src: '../fonts/lexend.woff2',
  display: 'swap',
  variable: '--font-lexend',
})

export const metadata: Metadata = {
  title: {
    template: '%s - Docs',
    default: 'LaunchFlow',
  },
  description: 'Python-native infrastructure for GCP, AWS, and Docker.',
  openGraph: {
    url: "https://www.launchflow.com",
    title: "LaunchFlow - Docs",
    description: "Python-native infrastructure for GCP, AWS, and Docker.",
    type: "website",
    images: [
      {
        url: "/images/environments_dark.png",
        width: 400,
        height: 400,
        alt: "LaunchFlow",
      },
    ],
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html
      lang="en"
      className={clsx('h-full antialiased', inter.variable, lexend.variable)}
      suppressHydrationWarning
    >
      <Suspense>
        <PostHogPageview />
      </Suspense>
      <PHProvider>
        <body className="flex min-h-full bg-white dark:bg-background_dark light">
          <Providers>
            <Layout>{children}</Layout>
          </Providers>
        </body>
      </PHProvider>
    </html>
  )
}

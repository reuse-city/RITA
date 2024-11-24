// frontend/src/components/shared/Layout.tsx
import Link from 'next/link';
import { useRouter } from 'next/router';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const router = useRouter();

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Knowledge Base', href: '/knowledge' },
    { name: 'Repair Cases', href: '/repair-cases' },
    { name: 'Community', href: '/community' },
    { name: 'Impact', href: '/impact' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="text-white font-bold text-xl">
                RITA
              </Link>
              <div className="hidden md:block ml-10">
                <div className="flex space-x-4">
                  {navigation.map((item) => {
                    const isActive = router.pathname === item.href;
                    return (
                      <Link
                        key={item.name}
                        href={item.href}
                        className={`${
                          isActive
                            ? 'bg-gray-900 text-white'
                            : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                        } px-3 py-2 rounded-md text-sm font-medium`}
                      >
                        {item.name}
                      </Link>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Content */}
      <main>{children}</main>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-300">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="md:flex md:justify-between">
            <div className="mb-8 md:mb-0">
              <h3 className="text-lg font-semibold mb-2">About RITA</h3>
              <p className="text-sm">
                Supporting repair communities and promoting reuse for a sustainable future.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-8 md:grid-cols-3">
              <div>
                <h3 className="text-lg font-semibold mb-2">Resources</h3>
                <ul className="text-sm space-y-2">
                  <li>
                    <Link href="/guides" className="hover:text-white">
                      Repair Guides
                    </Link>
                  </li>
                  <li>
                    <Link href="/learning" className="hover:text-white">
                      Learning Resources
                    </Link>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">Community</h3>
                <ul className="text-sm space-y-2">
                  <li>
                    <Link href="/repair-cafes" className="hover:text-white">
                      Repair Cafés
                    </Link>
                  </li>
                  <li>
                    <Link href="/professionals" className="hover:text-white">
                      Professionals
                    </Link>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">Documentation</h3>
                <ul className="text-sm space-y-2">
                  <li>
                    <Link href="/docs" className="hover:text-white">
                      API Docs
                    </Link>
                  </li>
                  <li>
                    <Link href="/contribute" className="hover:text-white">
                      Contribute
                    </Link>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

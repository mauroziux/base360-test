import React, { useEffect, useState } from "react";
import { RevenueSummary } from "./RevenueSummary";
import { SecureAPI } from "../lib/secureApi";

interface Property {
  id: string;
  name: string;
  timezone: string;
}

const Dashboard: React.FC = () => {
  const [properties, setProperties] = useState<Property[]>([]);
  const [selectedProperty, setSelectedProperty] = useState<string>();
  const [error, setError] = useState<string>();

  useEffect(() => {
    let active = true;

    const loadProperties = async () => {
      try {
        const result = await SecureAPI.getDashboardProperties();
        if (!active) return;
        setProperties(result);
        setSelectedProperty((current) => current && result.some((p) => p.id === current)
          ? current
          : result[0]?.id);
      } catch (loadError) {
        if (active) {
          setError("Failed to load properties");
          console.error(loadError);
        }
      }
    };

    loadProperties();
    return () => {
      active = false;
    };
  }, []);

  return (
    <div className="p-4 lg:p-6 min-h-full">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold mb-6 text-gray-900">Property Management Dashboard</h1>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 lg:p-6">
          <div className="mb-6">
            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
              <div>
                <h2 className="text-lg lg:text-xl font-medium text-gray-900 mb-2">Revenue Overview</h2>
                <p className="text-sm lg:text-base text-gray-600">
                  Monthly performance insights for your properties
                </p>
              </div>

              <div className="flex flex-col sm:items-end">
                <label className="text-xs font-medium text-gray-700 mb-1">Select Property</label>
                <select
                  value={selectedProperty || ""}
                  onChange={(event) => setSelectedProperty(event.target.value)}
                  disabled={!properties.length}
                  className="block w-full sm:w-auto min-w-[200px] px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
                >
                  {!properties.length && <option value="">Loading properties...</option>}
                  {properties.map((property) => (
                    <option key={`${property.id}-${property.timezone}`} value={property.id}>
                      {property.name}
                    </option>
                  ))}
                </select>
                {error && <p className="text-xs text-red-600 mt-1">{error}</p>}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            {selectedProperty && <RevenueSummary propertyId={selectedProperty} />}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

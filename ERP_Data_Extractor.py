"""
ERP Data Extractor
Handles data extraction from ERP database
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional
# import pyodbc  # Uncomment when connecting to real SQL Server

logger = logging.getLogger(__name__)

class ERPDataExtractor:
    """Extract data from ERP system"""
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize the data extractor
        
        Args:
            connection_string: SQL Server connection string
        """
        self.connection_string = connection_string
        self.conn = None
        logger.info("ERPDataExtractor initialized")
        
        # For demo purposes, we'll generate dummy data
        # In production, uncomment the connection code below
        
        # if connection_string:
        #     self._connect()
    
    def _connect(self):
        """Establish database connection"""
        try:
            # Uncomment for real SQL Server connection
            # self.conn = pyodbc.connect(self.connection_string)
            # logger.info("Successfully connected to ERP database")
            pass
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise
    
    def _execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute SQL query and return DataFrame
        
        Args:
            query: SQL query string
            
        Returns:
            DataFrame with query results
        """
        try:
            # Uncomment for real database queries
            # return pd.read_sql(query, self.conn)
            pass
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
    
    def get_purchase_data(self) -> pd.DataFrame:
        """
        Extract purchase order data
        
        Returns:
            DataFrame with purchase data
        """
        logger.info("Fetching purchase data...")
        
        # Demo data generation - Replace with actual SQL query in production
        # query = """
        # SELECT 
        #     po_id, vendor_name, item_name, quantity, 
        #     unit_price, amount, order_date, delivery_date, status
        # FROM purchase_orders
        # WHERE order_date >= DATEADD(day, -30, GETDATE())
        # """
        # return self._execute_query(query)
        
        # Generate dummy data
        np.random.seed(42)
        n_records = 50
        
        data = {
            'po_id': [f'PO{str(i).zfill(4)}' for i in range(1, n_records + 1)],
            'vendor_name': np.random.choice(['Vendor A', 'Vendor B', 'Vendor C', 'Vendor D'], n_records),
            'item_name': np.random.choice(['Raw Material A', 'Raw Material B', 'Component X', 'Component Y'], n_records),
            'quantity': np.random.randint(100, 1000, n_records),
            'unit_price': np.random.uniform(10, 100, n_records).round(2),
            'order_date': [datetime.now() - timedelta(days=np.random.randint(0, 30)) for _ in range(n_records)],
            'delivery_date': [datetime.now() + timedelta(days=np.random.randint(1, 15)) for _ in range(n_records)],
            'status': np.random.choice(['Pending', 'Approved', 'Delivered'], n_records, p=[0.3, 0.4, 0.3])
        }
        
        df = pd.DataFrame(data)
        df['amount'] = (df['quantity'] * df['unit_price']).round(2)
        
        logger.info(f"Retrieved {len(df)} purchase records")
        return df
    
    def get_production_data(self) -> pd.DataFrame:
        """
        Extract production data
        
        Returns:
            DataFrame with production data
        """
        logger.info("Fetching production data...")
        
        # Demo data generation
        np.random.seed(43)
        n_records = 60
        
        data = {
            'production_id': [f'PROD{str(i).zfill(4)}' for i in range(1, n_records + 1)],
            'product_name': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], n_records),
            'batch_no': [f'B{str(i).zfill(3)}' for i in range(1, n_records + 1)],
            'quantity': np.random.randint(500, 5000, n_records),
            'unit': np.random.choice(['KG', 'PCS', 'LTR'], n_records),
            'start_date': [datetime.now() - timedelta(days=np.random.randint(0, 20)) for _ in range(n_records)],
            'end_date': [datetime.now() + timedelta(days=np.random.randint(1, 10)) for _ in range(n_records)],
            'status': np.random.choice(['Completed', 'In Progress', 'Pending'], n_records, p=[0.5, 0.3, 0.2]),
            'department': np.random.choice(['Dept A', 'Dept B', 'Dept C'], n_records)
        }
        
        df = pd.DataFrame(data)
        logger.info(f"Retrieved {len(df)} production records")
        return df
    
    def get_packing_data(self) -> pd.DataFrame:
        """
        Extract packing data
        
        Returns:
            DataFrame with packing data
        """
        logger.info("Fetching packing data...")
        
        # Demo data generation
        np.random.seed(44)
        n_records = 45
        
        data = {
            'packing_id': [f'PACK{str(i).zfill(4)}' for i in range(1, n_records + 1)],
            'product_name': np.random.choice(['Product A', 'Product B', 'Product C'], n_records),
            'quantity': np.random.randint(100, 1000, n_records),
            'package_type': np.random.choice(['Box', 'Carton', 'Pallet'], n_records),
            'packing_date': [datetime.now() - timedelta(days=np.random.randint(0, 15)) for _ in range(n_records)],
            'status': np.random.choice(['Completed', 'In Progress', 'Pending'], n_records, p=[0.6, 0.25, 0.15]),
            'operator': np.random.choice(['Operator 1', 'Operator 2', 'Operator 3'], n_records)
        }
        
        df = pd.DataFrame(data)
        logger.info(f"Retrieved {len(df)} packing records")
        return df
    
    def get_shipment_data(self) -> pd.DataFrame:
        """
        Extract shipment data
        
        Returns:
            DataFrame with shipment data
        """
        logger.info("Fetching shipment data...")
        
        # Demo data generation
        np.random.seed(45)
        n_records = 40
        
        data = {
            'shipment_id': [f'SHIP{str(i).zfill(4)}' for i in range(1, n_records + 1)],
            'customer_name': np.random.choice(['Customer A', 'Customer B', 'Customer C', 'Customer D'], n_records),
            'destination': np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'], n_records),
            'quantity': np.random.randint(50, 500, n_records),
            'shipment_date': [datetime.now() - timedelta(days=np.random.randint(0, 10)) for _ in range(n_records)],
            'expected_delivery': [datetime.now() + timedelta(days=np.random.randint(1, 7)) for _ in range(n_records)],
            'status': np.random.choice(['Dispatched', 'In Transit', 'Pending', 'Delivered'], n_records, p=[0.3, 0.3, 0.2, 0.2]),
            'transporter': np.random.choice(['Transport A', 'Transport B', 'Transport C'], n_records)
        }
        
        df = pd.DataFrame(data)
        logger.info(f"Retrieved {len(df)} shipment records")
        return df
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")


# Example SQL queries for real ERP integration:
"""
-- Purchase Orders Query
SELECT 
    po.purchase_order_id as po_id,
    v.vendor_name,
    i.item_name,
    pod.quantity,
    pod.unit_price,
    pod.quantity * pod.unit_price as amount,
    po.order_date,
    po.delivery_date,
    po.status
FROM purchase_orders po
JOIN purchase_order_details pod ON po.purchase_order_id = pod.purchase_order_id
JOIN vendors v ON po.vendor_id = v.vendor_id
JOIN items i ON pod.item_id = i.item_id
WHERE po.order_date >= DATEADD(day, -30, GETDATE())

-- Production Query
SELECT 
    p.production_id,
    pr.product_name,
    p.batch_no,
    p.quantity,
    p.unit,
    p.start_date,
    p.end_date,
    p.status,
    d.department_name as department
FROM production p
JOIN products pr ON p.product_id = pr.product_id
JOIN departments d ON p.department_id = d.department_id
WHERE p.start_date >= DATEADD(day, -20, GETDATE())

-- Packing Query
SELECT 
    pk.packing_id,
    pr.product_name,
    pk.quantity,
    pk.package_type,
    pk.packing_date,
    pk.status,
    e.employee_name as operator
FROM packing pk
JOIN products pr ON pk.product_id = pr.product_id
JOIN employees e ON pk.operator_id = e.employee_id
WHERE pk.packing_date >= DATEADD(day, -15, GETDATE())

-- Shipment Query
SELECT 
    s.shipment_id,
    c.customer_name,
    s.destination,
    s.quantity,
    s.shipment_date,
    s.expected_delivery,
    s.status,
    t.transporter_name as transporter
FROM shipments s
JOIN customers c ON s.customer_id = c.customer_id
JOIN transporters t ON s.transporter_id = t.transporter_id
WHERE s.shipment_date >= DATEADD(day, -10, GETDATE())
"""
